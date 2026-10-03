from __future__ import annotations

"""Autonomous programming maintenance loop.

The loop runs on the production PythonAnywhere project. It:
1) pulls additive updates from GitHub when the working tree is clean,
2) compiles/tests the project,
3) asks Claude to review the resulting repository state when configured,
4) records truthful activity and blocks unsafe merges when review/evidence is missing.

It never stores API secrets in Git and never claims a deployment/review happened without proof.
"""

import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .programming_workforce import activate_and_audit

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "data" / "programming_autopilot.json"
ACTIVITY_PATH = ROOT / "data" / "programming_activity.jsonl"
REPO = os.getenv("ORVIA_GITHUB_REPO", "origin")
BRANCH = os.getenv("ORVIA_GITHUB_BRANCH", "main")
TEST_TIMEOUT = int(os.getenv("ORVIA_CODE_TEST_TIMEOUT", "300"))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def _log(event: str, status: str, detail: Any = None) -> None:
    record = {"timestamp": _now(), "event": event, "status": status}
    if detail is not None:
        record["detail"] = str(detail)[:12000]
    ACTIVITY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ACTIVITY_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def _run(*args: str, timeout: int = 60) -> tuple[int, str]:
    proc = subprocess.run(
        list(args), cwd=ROOT, text=True, capture_output=True,
        timeout=timeout, check=False,
    )
    output = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    return proc.returncode, output[-20000:]


def git_status() -> str:
    code, out = _run("git", "status", "--porcelain", timeout=30)
    if code:
        raise RuntimeError(out)
    return out


def git_sync() -> dict[str, Any]:
    before = _run("git", "rev-parse", "HEAD", timeout=30)[1]
    dirty = git_status()
    if dirty:
        return {"status": "blocked_dirty_tree", "before": before, "dirty": dirty}
    code, out = _run("git", "fetch", REPO, BRANCH, timeout=120)
    if code:
        return {"status": "fetch_failed", "detail": out}
    code, behind = _run("git", "rev-list", "--count", f"HEAD..{REPO}/{BRANCH}", timeout=30)
    if code:
        return {"status": "compare_failed", "detail": behind}
    count = int(behind.strip() or "0")
    if count:
        code, pull = _run("git", "pull", "--ff-only", REPO, BRANCH, timeout=180)
        if code:
            return {"status": "pull_failed", "detail": pull, "updates": count}
        after = _run("git", "rev-parse", "HEAD", timeout=30)[1]
        _log("github_sync", "updated", f"{count} commit(s): {before[:12]} -> {after[:12]}")
        return {"status": "updated", "updates": count, "before": before, "after": after}
    return {"status": "up_to_date", "updates": 0, "commit": before}


def run_verification() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    code, out = _run("python", "-m", "compileall", "-q", "app", "scripts", timeout=TEST_TIMEOUT)
    checks.append({"name": "compileall", "ok": code == 0, "output": out})
    pytest = _run("python", "-m", "pytest", "-q", timeout=TEST_TIMEOUT)
    checks.append({"name": "pytest", "ok": pytest[0] == 0, "output": pytest[1]})
    return {"ok": all(x["ok"] for x in checks), "checks": checks}


def claude_review(summary: str) -> dict[str, Any]:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return {"status": "not_configured", "provider": "claude"}
    import urllib.request

    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    prompt = (
        "You are ORVIA's senior code reviewer. Review the following production "
        "programming-agent result. Return JSON with keys: decision (APPROVE, "
        "REQUEST_CHANGES, BLOCKED), critical_issues, required_fixes, and summary. "
        "Do not claim tests or deployment that are not shown.\n\n" + summary
    )
    body = json.dumps({
        "model": model,
        "max_tokens": 1800,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            payload = json.loads(response.read().decode())
        text = "".join(
            block.get("text", "") for block in payload.get("content", [])
            if isinstance(block, dict)
        )
        return {"status": "reviewed", "provider": "claude", "model": model, "review": text}
    except Exception as exc:
        return {"status": "review_failed", "provider": "claude", "error": f"{type(exc).__name__}: {exc}"}


def run_once() -> dict[str, Any]:
    state: dict[str, Any] = {"timestamp": _now(), "phase": "programming_workforce_activation"}
    try:
        workforce = activate_and_audit()
        state["programming_workforce"] = {
            "status": workforce.get("status"),
            "agents_dispatched": workforce.get("workforce", {}).get("agents_dispatched"),
            "agents_completed": workforce.get("workforce", {}).get("agents_completed"),
        }
        state["phase"] = "github_sync"
        sync = git_sync()
        state["github"] = sync
        if sync["status"] == "blocked_dirty_tree":
            _log("sync", "blocked", sync["dirty"])
            return state
        verification = run_verification()
        state["verification"] = verification
        review_input = json.dumps(
            {"github": sync, "verification": verification, "commit": _run("git", "rev-parse", "HEAD")[1]},
            ensure_ascii=False,
        )
        review = claude_review(review_input)
        state["claude_review"] = review
        if not verification["ok"]:
            state["status"] = "needs_programming_agent_fix"
            _log("verification", "failed", verification)
        elif review["status"] == "reviewed":
            state["status"] = "verified_by_claude" if "APPROVE" in review.get("review", "") else "claude_review_action_required"
            _log("claude_review", state["status"], review.get("review"))
        else:
            state["status"] = "waiting_for_claude_review"
            _log("claude_review", "blocked", review.get("status"))
        _write_json(STATE_PATH, state)
        return state
    except Exception as exc:
        state["status"] = "error"
        state["error"] = f"{type(exc).__name__}: {exc}"
        _write_json(STATE_PATH, state)
        _log("autopilot", "error", state["error"])
        return state
