from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from .agent_bus import agent_bus

CHANNEL_ID = "lumíkids"
CHANNEL_URL = "https://www.youtube.com/@LumiKidsTV-b3e"

@dataclass(frozen=True)
class LumiAgent:
    id: str
    role: str
    department: str
    responsibility: str

_ROLE_DATA = [
("01","Channel Director","Leadership","sets objectives, priorities and daily operating plan"),
("02","Trend Scout","Research","detects rising public kids-video topics, formats and patterns"),
("03","Competitor Analyst","Research","compares public competitor channels, videos and publishing patterns"),
("04","Audience Analyst","Research","studies audience needs, age fit and viewing behavior"),
("05","Keyword Researcher","Discovery","finds search topics, phrases and content opportunities"),
("06","Trend Pattern Miner","Discovery","extracts reusable structural patterns without copying protected works"),
("07","Content Strategist","Content","turns research into a weekly content portfolio"),
("08","Song Concept Designer","Content","creates original song concepts and hooks"),
("09","Lyric Writer","Music","writes original age-appropriate lyrics"),
("10","Music Composer","Music","creates original melodies, arrangements and musical direction"),
("11","Rhyme Specialist","Music","optimizes rhythm, repetition and sing-along structure"),
("12","Early Learning Designer","Education","maps songs to age-appropriate learning goals"),
("13","Story Writer","Story","writes original short stories and narratives"),
("14","Storyboard Artist","Visual","converts scripts into scene-by-scene storyboards"),
("15","Character Designer","Visual","maintains original recurring character identities"),
("16","Art Director","Visual","defines visual language, composition and scene consistency"),
("17","Animation Planner","Production","plans animation shots, motion and timing"),
("18","AI Video Producer","Production","coordinates AI-assisted video generation workflows"),
("19","Voice Director","Audio","selects voice direction, pacing and child-friendly delivery"),
("20","Voice Production","Audio","prepares authorized synthetic or recorded narration/voices"),
("21","Sound Designer","Audio","adds original sound effects and audio atmosphere"),
("22","Music Editor","Audio","syncs music, vocals and timing"),
("23","Video Editor","Post Production","assembles scenes, audio, captions and transitions"),
("24","Retention Editor","Post Production","optimizes openings, pacing and retention structure"),
("25","Quality Controller","Quality","checks audio, video, spelling, continuity and technical quality"),
("26","Child Safety Reviewer","Safety","checks age suitability, safety and family-friendly presentation"),
("27","Copyright/IP Reviewer","Safety","screens concepts and assets for copying or protected material"),
("28","Thumbnail Designer","Packaging","creates original high-clarity thumbnail concepts"),
("29","Title Optimizer","Packaging","generates searchable, accurate and child-safe titles"),
("30","Description/Tags SEO","Packaging","optimizes descriptions, metadata and search terms"),
("31","Localization Manager","Growth","prepares subtitles, metadata and localization opportunities"),
("32","Shorts Producer","Growth","repurposes original channel content into Shorts safely"),
("33","Publishing Manager","Operations","prepares upload metadata, playlists and schedules"),
("34","YouTube Operations Agent","Operations","manages authorized YouTube Studio workflows"),
("35","Analytics Analyst","Analytics","tracks views, CTR, retention, watch time and engagement"),
("36","Experiment Manager","Analytics","designs controlled title, thumbnail and format experiments"),
("37","Content Performance Analyst","Analytics","connects video results to content attributes"),
("38","Recommendation Analyst","Analytics","studies public recommendation and discovery signals"),
("39","Comment/Community Manager","Community","moderates and organizes authorized audience interactions"),
("40","Trend-to-Content Planner","Strategy","turns validated trends into original production briefs"),
("41","Catalog Manager","Library","organizes videos, playlists, series and reusable assets"),
("42","Production Scheduler","Operations","balances daily production queues and deadlines"),
("43","Cost Controller","Operations","tracks generation/editing costs and resource usage"),
("44","Monetization Analyst","Revenue","analyzes eligible monetization and revenue opportunities"),
("45","Partnership Analyst","Revenue","finds potential brand/collaboration opportunities"),
("46","Learning Agent","Learning","learns from performance feedback and updates playbooks"),
("47","Automation Engineer","Automation","turns repeatable channel workflows into automations"),
("48","Recovery/Backup Agent","Reliability","protects plans, metadata and production state"),
("49","Daily Report Agent","Reporting","produces categorized daily executive reports"),
("50","Final Approver","Governance","runs final policy/quality checks before external publishing"),
]

LUMIKIDS_AGENTS = [LumiAgent(f"lumikids_{n}", role, dept, responsibility) for n, role, dept, responsibility in _ROLE_DATA]

class LumiKidsAutonomousStudio:
    def __init__(self) -> None:
        self.agents = {a.id: a for a in LUMIKIDS_AGENTS}
        self.cycles: list[dict[str, Any]] = []

    def status(self) -> dict[str, Any]:
        return {
            "channel_id": CHANNEL_ID,
            "channel_url": CHANNEL_URL,
            "agents": len(self.agents),
            "autonomous_scope": [
                "trend_research", "competitor_analysis", "content_strategy", "song_creation",
                "lyrics", "music", "story", "storyboard", "characters", "animation",
                "voice", "sound", "editing", "quality", "safety", "copyright_review",
                "thumbnail", "title", "seo", "shorts", "publishing", "analytics",
                "experiments", "community", "catalog", "scheduling", "costs", "monetization",
                "learning", "automation", "backup", "daily_reporting",
            ],
            "publishing_mode": "authorized_youtube_connection_required",
            "copy_policy": "use trends as signals; create original concepts, scripts, music, visuals and edits; never clone protected works",
        }

    def plan_cycle(self, topic: str = "daily trending kids content") -> dict[str, Any]:
        if not topic.strip():
            raise ValueError("topic is required")
        now = datetime.now(timezone.utc).isoformat()
        phases = [
            ("research", ["lumikids_02","lumikids_03","lumikids_04","lumikids_05","lumikids_06"]),
            ("strategy", ["lumikids_07","lumikids_12","lumikids_40"]),
            ("creation", ["lumikids_08","lumikids_09","lumikids_10","lumikids_11","lumikids_13","lumikids_14","lumikids_15","lumikids_16"]),
            ("production", ["lumikids_17","lumikids_18","lumikids_19","lumikids_20","lumikids_21","lumikids_22","lumikids_23","lumikids_24"]),
            ("review", ["lumikids_25","lumikids_26","lumikids_27"]),
            ("packaging", ["lumikids_28","lumikids_29","lumikids_30","lumikids_31","lumikids_32"]),
            ("publish", ["lumikids_33","lumikids_34"]),
            ("measure", ["lumikids_35","lumikids_36","lumikids_37","lumikids_38"]),
            ("community", ["lumikids_39"]),
            ("operations", ["lumikids_41","lumikids_42","lumikids_43","lumikids_44","lumikids_45","lumikids_46","lumikids_47","lumikids_48","lumikids_49","lumikids_50"]),
        ]
        result = {"started_at": now, "topic": topic.strip(), "channel_id": CHANNEL_ID, "phases": []}
        for phase, ids in phases:
            recipients = [x for x in ids if x in self.agents]
            for recipient in recipients:
                agent_bus.send("lumikids_director", recipient, phase, {"channel_id": CHANNEL_ID, "topic": topic.strip()})
            result["phases"].append({"phase": phase, "agents": recipients, "count": len(recipients)})
        result["total_assigned"] = sum(x["count"] for x in result["phases"])
        self.cycles.append(result)
        return result

    def daily_report(self) -> dict[str, Any]:
        return {
            "channel": CHANNEL_ID,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "team_size": len(self.agents),
            "communication_messages": len(agent_bus.messages),
            "last_cycle": self.cycles[-1] if self.cycles else None,
            "categories": [
                "trends_and_competitors", "content_and_music", "production_and_editing",
                "quality_safety_copyright", "publishing_and_seo", "analytics_and_growth",
                "community", "operations_and_revenue", "learning_and_automation",
            ],
        }

lumikids_studio = LumiKidsAutonomousStudio()
