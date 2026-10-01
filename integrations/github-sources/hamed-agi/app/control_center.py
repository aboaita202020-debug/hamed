from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .core import core
from .crm import crm
from .memory_store import memory_store
from .models import Mission
from .opportunity import opportunity_engine
from .revenue import revenue_engine
from .sentinel import sentinel
from .tooling import tool_registry


def daily_control_report() -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    mission = Mission(objective="daily control report")
    opportunities = opportunity_engine.discover(mission)
    return {
        "generated_at": now,
        "system": {
            "health": core.health(),
            "memory_entries": len(memory_store.recent(500)),
            "tools_registered": len(tool_registry.list()),
        },
        "executive_summary": {
            "opportunities": len(opportunities),
            "crm": crm.summary(),
            "revenue": revenue_engine.summary(),
        },
        "security": sentinel.status(),
        "sections": {
            "commercial_opportunities": [x.model_dump() for x in opportunities],
            "customers_and_sales": crm.summary(),
            "security_and_threat_intel": sentinel.status(),
            "learning": {"memory_entries": len(memory_store.recent(500))},
            "infrastructure": core.health(),
        },
        "next_actions": [
            "review verified high-risk findings",
            "qualify new commercial opportunities",
            "follow up on open CRM leads",
            "verify unresolved findings before outreach",
        ],
    }
