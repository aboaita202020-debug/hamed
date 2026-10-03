from __future__ import annotations
from pathlib import Path
import json
from .orchestrator import orchestrator
from .core import core
from .agent_bus import agent_bus
from .programming_workforce import status as programming_workforce_status
from .provider_router import provider_router
from .cognitive_core import cognitive_core

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "data" / "autonomous_state.json"
ACTIVITY = ROOT / "data" / "agent_activity.jsonl"

def _json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def snapshot():
    state = _json(STATE)
    try:
        lines = ACTIVITY.read_text(encoding="utf-8").splitlines()[-60:]
        activity = [json.loads(x) for x in reversed(lines) if x.strip()]
    except Exception:
        activity = []
    latest = {}
    for item in activity:
        agent = item.get("agent")
        if agent and agent not in latest:
            latest[agent] = item
    active = [x for x in latest.values() if x.get("event") == "started"]
    return {
        "status": "ok",
        "service": "ORVIA Mobile Control Center",
        "orvia": core.health(),
        "agents": {
            "total": len(orchestrator.agents),
            "active": len(active),
            "active_agents": active[:100],
        },
        "autonomous": state,
        "programming_workforce": programming_workforce_status(),
        "providers": [x.__dict__ for x in provider_router.states()],
        "cognitive": cognitive_core.status(),
        "intelligence_benchmark": cognitive_core.benchmark(),
        "agent_messages": agent_bus.status().get("messages", 0),
        "activity": activity,
    }

def manifest():
    return {
        "name": "ORVIA AGI Mobile Control Center",
        "short_name": "ORVIA",
        "start_url": "/mobile",
        "display": "standalone",
        "background_color": "#0b1020",
        "theme_color": "#151d33",
        "lang": "ar",
        "dir": "rtl",
        "description": "Live mobile control center for ORVIA AGI"
    }
