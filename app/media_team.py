from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .agent_bus import agent_bus
from .memory_store import memory_store

CHANNEL_IDS = ("kids", "english_school", "islamic_english")

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class MediaAgent:
    agent_id: str
    channel_id: str
    specialty: str
    group: str

@dataclass
class MediaRun:
    run_id: str
    channel_id: str
    topic: str
    proposals: list[dict[str, Any]] = field(default_factory=list)
    selected: dict[str, Any] | None = None
    stages: list[str] = field(default_factory=list)
    status: str = "planning"

GROUPS = {
    "discovery": ["idea_discovery","trend_research","audience_research","competitor_analysis","content_gap_analysis"],
    "editorial": ["topic_editor","story_editor","script_writer","hook_writer","fact_checker"],
    "audio": ["lyrics","composer","voice_director","sound_design","audio_quality"],
    "visual": ["character_design","art_direction","storyboard","animation_plan","scene_continuity"],
    "production": ["video_generation","asset_manager","editor","subtitle_editor","render_quality"],
    "safety": ["child_safety","copyright_review","brand_safety","cultural_review","final_quality"],
    "growth": ["title_seo","description_seo","thumbnail","metadata","packaging"],
    "publishing": ["upload_manager","schedule_manager","playlist_manager","channel_manager","publishing_audit"],
    "analytics": ["performance_analyst","retention_analyst","engagement_analyst","experiment_analyst","next_topic_analyst"],
    "learning": ["lesson_extractor","failure_analyzer","process_optimizer","memory_curator","team_coordinator"],
}

def _build_agents(channel_id: str) -> list[MediaAgent]:
    return [
        MediaAgent(f"media-{channel_id}-{group}-{specialty}-{slot:02d}", channel_id, specialty, group)
        for group, specialties in GROUPS.items()
        for specialty in specialties
        for slot in range(1, 6)
    ]

class MediaProductionTeam:
    def __init__(self) -> None:
        self.agents = {channel_id: _build_agents(channel_id) for channel_id in CHANNEL_IDS}
        self.runs: list[MediaRun] = []

    def status(self) -> dict[str, Any]:
        return {
            "channels": len(self.agents),
            "agents_per_channel": {k: len(v) for k, v in self.agents.items()},
            "total_media_agents": sum(len(v) for v in self.agents.values()),
            "autonomous_workflow": True,
            "publishing": "authorized_connection_required",
            "voice": "production_stage",
            "editing": "production_stage",
            "safety_gate": "mandatory",
            "truth_model": "planned != executed != published != verified",
        }

    def channel_agents(self, channel_id: str) -> list[dict[str, str]]:
        if channel_id not in self.agents:
            raise ValueError("unknown channel")
        return [a.__dict__ for a in self.agents[channel_id]]

    def propose(self, channel_id: str, topic: str | None = None) -> list[dict[str, Any]]:
        if channel_id not in self.agents:
            raise ValueError("unknown channel")
        base = (topic or "daily content opportunity").strip()
        proposals = [
            {"agent_id": a.agent_id, "specialty": a.specialty, "group": a.group,
             "proposal": f"{base}: propose a practical angle for {a.specialty}", "created_at": _now()}
            for a in self.agents[channel_id]
        ]
        agent_bus.broadcast("media_director", "daily_proposals",
                            {"channel_id": channel_id, "count": len(proposals)},
                            [a.agent_id for a in self.agents[channel_id]])
        return proposals

    def start_daily_run(self, channel_id: str, topic: str) -> MediaRun:
        if channel_id not in self.agents:
            raise ValueError("unknown channel")
        if not topic.strip():
            raise ValueError("topic is required")
        proposals = self.propose(channel_id, topic)
        selected = next((p for p in proposals if p["group"] == "editorial"), proposals[0])
        run = MediaRun(
            run_id=f"media-{channel_id}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
            channel_id=channel_id, topic=topic.strip(), proposals=proposals, selected=selected,
            stages=["research","concept_selection","script","lyrics_or_story","voice_audio",
                    "visual_generation","editing","safety_review","thumbnail_metadata",
                    "publish_or_schedule","analytics","learning"],
            status="ready_for_production")
        self.runs.append(run)
        memory_store.record("media_run",
                            {"run_id": run.run_id, "channel_id": channel_id,
                             "topic": run.topic, "selected": selected},
                            source="media_production_team")
        return run

    def complete_stage(self, run_id: str, stage: str, result: dict[str, Any] | None = None) -> dict[str, Any]:
        run = next((r for r in self.runs if r.run_id == run_id), None)
        if run is None:
            raise ValueError("unknown run")
        if stage not in run.stages:
            raise ValueError("unknown stage")
        agent_bus.broadcast("media_director", "stage_completed",
                            {"run_id": run_id, "stage": stage, "result": result or {}},
                            [a.agent_id for a in self.agents[run.channel_id]])
        if stage == "learning":
            run.status = "completed"
        return {"run_id": run_id, "stage": stage, "status": run.status, "result": result or {}}

    def latest(self) -> dict[str, Any] | None:
        return self.runs[-1].__dict__ if self.runs else None

media_team = MediaProductionTeam()
