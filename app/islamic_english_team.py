from dataclasses import dataclass
from datetime import datetime, timezone
from .agent_bus import agent_bus

CHANNEL_ID = "islamic_english"

@dataclass(frozen=True)
class IslamicAgent:
    id: str
    role: str
    department: str

_ROLES = [(f"{i:02d}", f"Islamic Media Assistant {i:02d}", "Islamic Media") for i in range(1, 51)]
ISLAMIC_AGENTS = [IslamicAgent(f"islamic_{n}", r, d) for n, r, d in _ROLES]

class IslamicEnglishStudio:
    def __init__(self):
        self.agents = {a.id: a for a in ISLAMIC_AGENTS}
        self.cycles = []

    def status(self):
        return {"channel_id": CHANNEL_ID, "agents": len(self.agents), "daily_master_video": {"count": 1, "target_duration_minutes": 5}, "post_publish_distribution": ["youtube_shorts", "instagram_reels", "facebook_reels", "tiktok"], "sources_required": True, "ai_disclosure_required": True, "publishing_mode": "authorized_youtube_connection_required"}

    def plan_daily_cycle(self, topic="daily Islamic English topic"):
        if not topic.strip(): raise ValueError("topic is required")
        phases = [("research", range(1,13)), ("content", range(13,25)), ("production", range(25,34)), ("packaging_compliance", range(34,41)), ("publish", range(41,42)), ("post_publish_reels", range(42,44)), ("measure", range(44,46)), ("community_learning", range(46,50)), ("final_approval", range(50,51))]
        result = {"started_at": datetime.now(timezone.utc).isoformat(), "topic": topic.strip(), "channel_id": CHANNEL_ID, "master_duration_minutes": 5, "phases": []}
        for phase, nums in phases:
            ids = [f"islamic_{n:02d}" for n in nums]
            for recipient in ids: agent_bus.send("islamic_director", recipient, phase, {"channel_id": CHANNEL_ID, "topic": topic.strip()})
            result["phases"].append({"phase": phase, "agents": ids, "count": len(ids)})
        result["total_assigned"] = sum(x["count"] for x in result["phases"])
        result["post_publish_trigger"] = "create Reels/Shorts after master publication"
        self.cycles.append(result)
        return result

    def daily_report(self):
        return {"channel_id": CHANNEL_ID, "team_size": len(self.agents), "last_cycle": self.cycles[-1] if self.cycles else None, "categories": ["research_sources", "content", "production", "publishing", "reels", "analytics", "learning"]}

islamic_english_studio = IslamicEnglishStudio()
