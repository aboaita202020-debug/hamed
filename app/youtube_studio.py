from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .media_team import media_team


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ChannelProfile:
    channel_id: str
    name: str
    audience: str
    language: str
    mission: str
    cadence: str
    content_pillars: tuple[str, ...]
    safety_policy: str


@dataclass
class ChannelPlan:
    channel_id: str
    date: str
    topic: str
    title_ideas: list[str]
    target_words: list[str]
    story_outline: list[str]
    visual_direction: list[str]
    production_steps: list[str]
    research_signals: dict[str, Any] = field(default_factory=dict)
    status: str = "planned"
    media_run_id: str | None = None
    media_agents: int = 0


CHANNELS = {
    "kids": ChannelProfile(
        channel_id="kids",
        name="ORVIA Kids",
        audience="children and families learning beginner English",
        language="English",
        mission="original cartoon songs and stories that teach practical English through repetition, context and play",
        cadence="daily",
        content_pillars=("songs", "cartoons", "stories", "beginner_english", "shorts"),
        safety_policy="child-safe, age-appropriate, original content; no copying protected characters or songs",
    ),
    "islamic_english": ChannelProfile(
        channel_id="islamic_english",
        name="ORVIA Islamic English",
        audience="English-speaking viewers in the United States and Europe",
        language="English",
        mission="clear, respectful and source-verified educational content about Islam",
        cadence="daily",
        content_pillars=("quran", "hadith", "prophets", "islam_basics", "new_muslims", "shorts"),
        safety_policy="source verification required; distinguish scripture, established scholarship and interpretation; respectful educational presentation",
    ),
}

# Public channel locations are optional configuration, not credentials.  Keeping
# this mapping separate lets the studio report channel metadata before a channel
# is connected for publishing or analytics.
CHANNEL_URLS = {
    "kids": "https://www.youtube.com/@LumiKidsTV-b3e",
    "islamic_english": None,
}


class YouTubeStudio:
    def __init__(self) -> None:
        self.plans: list[ChannelPlan] = []
        self.analytics: list[dict[str, Any]] = []
        self.research: list[dict[str, Any]] = []

    def channels(self) -> list[dict[str, Any]]:
        return [
            {"channel_id": c.channel_id, "name": c.name, "audience": c.audience, "language": c.language, "mission": c.mission, "cadence": c.cadence, "content_pillars": list(c.content_pillars), "safety_policy": c.safety_policy, "url": CHANNEL_URLS.get(c.channel_id), "media_agents": len(media_team.agents.get(c.channel_id, []))}
            for c in CHANNELS.values()
        ]

    def research_signals(self, channel_id: str, signals: dict[str, Any]) -> dict[str, Any]:
        if channel_id not in CHANNELS:
            raise ValueError("unknown channel")
        item = {"channel_id": channel_id, "captured_at": _now(), **signals}
        self.research.append(item)
        return item

    def create_daily_plan(self, channel_id: str, topic: str, *, target_words: list[str] | None = None, research_signals: dict[str, Any] | None = None) -> ChannelPlan:
        channel = CHANNELS.get(channel_id)
        if channel is None:
            raise ValueError("unknown channel")
        if not topic.strip():
            raise ValueError("topic is required")
        if channel_id == "kids":
            words = target_words or ["hello", "friend", "play", "learn", "happy"]
            titles = [f"{topic} | English Song for Kids", f"Let's Learn {topic} | Kids Cartoon Song", f"{topic} Adventure | Learn English with ORVIA Kids"]
            outline = ["Introduce one simple idea.", "Repeat target words with matching actions.", "Use the words in short sentences.", "End with a playful recap."]
            visuals = ["Original recurring characters.", "One clear visual action for each target word.", "Readable on-screen English words.", "Simple scene changes synchronized to the song."]
        else:
            words = target_words or []
            titles = [f"{topic} â€” An Introduction to Islam", f"What Islam Teaches About {topic}", f"{topic} Explained Clearly in English"]
            outline = ["Define the topic in plain English.", "Present primary sources and citations.", "Separate established facts from interpretation.", "Close with a concise recap and source list."]
            visuals = ["Respectful documentary-style visuals.", "On-screen source references.", "No sensationalized religious imagery.", "Clear English subtitles."]
        media_run = media_team.start_daily_run(channel_id, topic)
        plan = ChannelPlan(
            channel_id=channel_id, date=_now()[:10], topic=topic.strip(), title_ideas=titles, target_words=words,
            story_outline=outline, visual_direction=visuals,
            production_steps=["trend_and_competitor_research", "source_or_lyrics_verification", "script_and_story", "visual_plan", "voice_and_audio", "edit_and_quality_review", "thumbnail_and_metadata", "publish_or_schedule", "post_publish_analytics", "learning_feedback"],
            research_signals=research_signals or {}, media_run_id=media_run.run_id, media_agents=len(media_team.agents[channel_id])
        )
        self.plans.append(plan)
        return plan

    def record_analytics(self, channel_id: str, video_id: str, metrics: dict[str, Any]) -> dict[str, Any]:
        if channel_id not in CHANNELS:
            raise ValueError("unknown channel")
        item = {"channel_id": channel_id, "video_id": video_id, "captured_at": _now(), **metrics}
        self.analytics.append(item)
        return item

    def media_status(self) -> dict[str, Any]:
        return media_team.status()

    def media_agents(self, channel_id: str) -> list[dict[str, str]]:
        return media_team.channel_agents(channel_id)

    def media_run(self, channel_id: str, topic: str) -> dict[str, Any]:
        return media_team.start_daily_run(channel_id, topic).__dict__

    def complete_media_stage(self, run_id: str, stage: str, result: dict[str, Any] | None = None) -> dict[str, Any]:
        return media_team.complete_stage(run_id, stage, result)

    def status(self) -> dict[str, Any]:
        return {
            "channels": len(CHANNELS), "plans": len(self.plans), "analytics_records": len(self.analytics), "research_records": len(self.research),
            "media_team": media_team.status(),
            "publishing": "ready_for_authorized_youtube_connection",
            "policy": "draft and production workflows are safe by default; external publishing requires authorized account connection",
        }


youtube_studio = YouTubeStudio()
