from __future__ import annotations

"""Autonomous discovery and admission layer for programming/AI tools.

This module discovers public tool/API candidates, evaluates their metadata,
and can register verified, non-destructive integrations. It never harvests
third-party secrets, bypasses CAPTCHA, quotas, authentication, or provider
controls. Account creation is only marked automatable when a provider
explicitly permits it.
"""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from .tooling import ToolSpec, tool_registry

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "data" / "tool_acquisition.json"


@dataclass(frozen=True)
class ToolCandidate:
    id: str
    name: str
    category: str
    source_url: str
    integration: str
    free_or_open_source: bool
    account_required: bool
    automated_signup_allowed: bool
    notes: str


CANDIDATES: tuple[ToolCandidate, ...] = (
    ToolCandidate("github", "GitHub", "code", "https://github.com", "git/github-api",
                  True, True, False, "Repository and collaboration platform; account actions remain provider-controlled."),
    ToolCandidate("git", "Git", "code", "https://git-scm.com", "local-cli",
                  True, False, True, "Open-source version control."),
    ToolCandidate("python", "Python", "runtime", "https://www.python.org", "runtime",
                  True, False, True, "Primary ORVIA engineering runtime."),
    ToolCandidate("openrouter", "OpenRouter", "llm-api", "https://openrouter.ai", "openai-compatible",
                  True, True, False, "Use only models/endpoints explicitly available to the account."),
    ToolCandidate("gemini-api", "Google Gemini API", "llm-api", "https://ai.google.dev", "openai-compatible",
                  True, True, False, "Free-tier availability and limits must be checked live."),
    ToolCandidate("groq", "Groq API", "llm-api", "https://console.groq.com", "openai-compatible",
                  True, True, False, "Free-tier availability and limits must be checked live."),
    ToolCandidate("cerebras", "Cerebras API", "llm-api", "https://cloud.cerebras.ai", "openai-compatible",
                  True, True, False, "Free-tier availability and limits must be checked live."),
)


def discover() -> list[dict[str, Any]]:
    configured = _configured_env_keys()
    return [
        {
            **asdict(candidate),
            "configured": candidate.id in configured,
            "secret_exposed": False,
            "status": "candidate",
        }
        for candidate in CANDIDATES
    ]


def _configured_env_keys() -> set[str]:
    import os
    mapping = {
        "openrouter": "OPENROUTER_API_KEY",
        "gemini-api": "GEMINI_API_KEY",
        "groq": "GROQ_API_KEY",
        "cerebras": "CEREBRAS_API_KEY",
        "github": "GITHUB_TOKEN",
    }
    return {key for key, env in mapping.items() if os.getenv(env)}


def register_verified_tool(
    *,
    name: str,
    category: str,
    description: str,
    source_url: str,
    requires_authorization: bool = False,
) -> dict[str, Any]:
    """Admit a tool only as a registered capability; execution still needs a handler."""
    tool_registry.register(
        ToolSpec(
            name=name,
            category=category,
            description=description,
            requires_authorization=requires_authorization,
            destructive=False,
        )
    )
    state = load_state()
    state.setdefault("registered", {})[name] = {
        "category": category,
        "description": description,
        "source_url": source_url,
        "registered_at": _now(),
        "verified": False,
        "handler_installed": False,
    }
    save_state(state)
    return {"status": "registered", "tool": name, "verified": False, "handler_installed": False}


def evaluate(candidate_id: str) -> dict[str, Any]:
    candidate = next((x for x in CANDIDATES if x.id == candidate_id), None)
    if candidate is None:
        return {"status": "not_found", "candidate": candidate_id}
    return {
        "status": "evaluated",
        "candidate": asdict(candidate),
        "admission_rules": [
            "official/public source",
            "license or terms reviewed",
            "no secret harvesting",
            "no quota/CAPTCHA bypass",
            "integration test required before activation",
        ],
    }


def status() -> dict[str, Any]:
    state = load_state()
    return {
        "status": "ok",
        "candidate_count": len(CANDIDATES),
        "configured_count": len(_configured_env_keys()),
        "registered_count": len(state.get("registered", {})),
        "registered": state.get("registered", {}),
        "truth_rule": "discovered != registered != verified != executable",
    }


def load_state() -> dict[str, Any]:
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"registered": {}, "updated_at": _now()}


def save_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = _now()
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
