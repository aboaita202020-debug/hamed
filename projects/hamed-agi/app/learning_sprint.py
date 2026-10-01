from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .rd_agents import rd_status, select_for_topic
from .universal_learning import universal_learning

DOMAINS = (
    "marketing", "marketing_psychology", "sales", "negotiation",
    "websites", "ecommerce", "ai", "software", "cybersecurity",
    "data", "content", "business", "education",
)

class LearningSprint:
    def run(self, topic: str = "ORVIA commercial intelligence") -> dict[str, Any]:
        plan = universal_learning.create_learning_plan(topic)
        return {
            "status": "planned",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "timebox_minutes": 60,
            "topic": topic,
            "domains": list(DOMAINS),
            "rd_network": rd_status(),
            "initial_team": select_for_topic(topic, 100),
            "pipeline": plan["pipeline"],
            "sources": plan["sources"],
            "note": "A one-hour sprint is an initial intensive learning cycle, not literal mastery of all human knowledge.",
        }

learning_sprint = LearningSprint()
