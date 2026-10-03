from __future__ import annotations

"""Programming Workforce command layer.

Activates the specialized engineering agents, assigns the first real engineering
audit, records truthful state, and keeps Claude in the supervisory/review role.
Agents currently produce evidence-backed engineering findings through the
existing orchestrator; this layer never fabricates code edits or deployments.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .orchestrator import orchestrator

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "data" / "programming_workforce.json"
ACTIVITY_PATH = ROOT / "data" / "programming_workforce.jsonl"

PROGRAMMING_ROLES = {
    "python engineer", "backend engineer", "frontend engineer",
    "DevOps engineer", "GitHub update engineer", "test engineer",
    "debugging engineer", "code review engineer", "deployment engineer",
    "LLM integration engineer", "free LLM researcher",
    "provider integration engineer", "self-healing engineer",
    "performance engineer", "security code auditor",
    "repository maintenance engineer", "software analyst",
    "web architect", "automation analyst", "QA analyst", "integration analyst",
}

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _write_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATE_PATH)

def _log(event: str, status: str, detail: Any = None) -> None:
    ACTIVITY_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {"timestamp": _now(), "event": event, "status": status}
    if detail is not None:
        record["detail"] = str(detail)[:12000]
    with ACTIVITY_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

def programming_agents() -> list[str]:
    agents = []
    for agent in orchestrator.agents.values():
        if agent.role in PROGRAMMING_ROLES or agent.department == "Websites & Software":
            agents.append(agent.name)
    return agents

def status() -> dict[str, Any]:
    names = programming_agents()
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        state = {"status": "not_activated"}
    return {
        "status": "ok",
        "workforce_status": state,
        "programming_agents_available": len(names),
        "programming_agents": names,
        "claude_role": "supervisor_architect_reviewer_quality_gate",
        "programming_role": "autonomous_engineering_execution",
        "truth_rule": "activation requires real task dispatch evidence",
    }

def activate_and_audit(objective: str | None = None, limit: int | None = None) -> dict[str, Any]:
    names = programming_agents()
    selected = names[:max(1, min(limit or len(names), len(names)))]
    audit_objective = objective or (
        "FULL ORVIA ENGINEERING AUDIT: inspect the current repository architecture, "
        "PythonAnywhere/runtime concerns, tests, APIs, agents, orchestrator, "
        "programming autopilot, providers/free-LLM integration, deployment, "
        "security, reliability, and identify concrete fixes or next engineering actions. "
        "Return evidence-backed findings; do not claim edits/deployments that were not performed."
    )
    state = {
        "status": "activated_and_dispatched",
        "activated_at": _now(),
        "claude_mode": "supervisory",
        "programming_authority": "broad_within_authorized_orvia_scope",
        "agents_available": len(names),
        "agents_dispatched": len(selected),
        "first_task": audit_objective,
    }
    _write_state(state)
    _log("workforce_activation", "started", {"agents": len(selected), "objective": audit_objective})
    results = orchestrator.collaborate(audit_objective, selected)
    completed = len(results)
    state["status"] = "active"
    state["agents_completed"] = completed
    state["last_dispatch_at"] = _now()
    state["last_results"] = [
        {"agent": r.get("agent"), "status": r.get("status")} for r in results[-100:]
    ]
    _write_state(state)
    _log("first_engineering_audit", "completed", {"requested": len(selected), "completed": completed})
    return {
        "status": "started",
        "workforce": state,
        "results": results,
        "handoff": {
            "implementation_owner": "programming_workforce",
            "supervisor": "claude",
            "next": "review_findings_then_return_changes_to_programming_agents",
        },
    }
