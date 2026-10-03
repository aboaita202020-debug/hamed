from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .media_team import media_team

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

CHANNEL_URLS = {
    "kids": "https://www.youtube.com/@LumiKidsTV-b3e",
    "english_school": None,
    "islamic_english": None,
}

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
        "kids", "LumiKidsTV", "children and families learning beginner English", "English",
        "original cartoon songs and stories that teach practical English through repetition, context and play",
        "daily", ("songs","cartoons","stories","beginner_english","shorts"),
        "child-safe, age-appropriate, original content; no copying protected characters or songs"),
    "english_school": ChannelProfile(
        "english_school", "English in School", "students and English learners", "English",
        "daily practical English learning through vocabulary, grammar, speaking and school situations",
        "daily", ("vocabulary","grammar","speaking","school_english","shorts"),
        "educational accuracy, age-appropriate language and original examples"),
    "islamic_english": ChannelProfile(
        "islamic_english", "English Islamic Content", "English-speaking viewers in the United States and Europe", "English",
        "clear, respectful and source-verified educational content about Islam",
        "daily", ("quran","hadith","prophets","islam_basics","new_muslims","shorts"),
        "source verification required; distinguish scripture, established scholarship and interpretation"),
}

class YouTubeStudio:
    def __init__(self) -> None:
        self.plans: list[ChannelPlan] = []
        self.analytics: list[dict[str, Any]] = []
        self.research: list[dict[str, Any]] = []
        self.execution_events: list[dict[str, Any]] = []

    def channels(self) -> list[dict[str, Any]]:
        return [
            {
                "channel_id": c.channel_id, "name": c.name, "audience": c.audience,
                "language": c.language, "mission": c.mission, "cadence": c.cadence,
                "content_pillars": list(c.content_pillars), "safety_policy": c.safety_policy,
                "url": CHANNEL_URLS.get(c.channel_id),
                "media_agents": len(media_team.agents.get(c.channel_id, [])),
                "connection_status": "authorized_connection_required",
            }
            for c in CHANNELS.values()
        ]

    def research_signals(self, channel_id: str, signals: dict[str, Any]) -> dict[str, Any]:
        self._require_channel(channel_id)
        item = {"channel_id": channel_id, "captured_at": _now(), **signals}
        self.research.append(item)
        return item

    def create_daily_plan(self, channel_id: str, topic: str, *, target_words: list[str] | None = None,
                          research_signals: dict[str, Any] | None = None) -> ChannelPlan:
        channel = self._get_channel(channel_id)
        if not topic.strip():
            raise ValueError("topic is required")
        if channel_id == "kids":
            words = target_words or ["hello", "friend", "play", "learn", "happy"]
            titles = [f"{topic} | English Song for Kids", f"Let's Learn {topic} | Kids Cartoon Song", f"{topic} Adventure | Learn English with ORVIA Kids"]
            outline = ["Introduce one simple idea.", "Repeat target words with matching actions.", "Use the words in short sentences.", "End with a playful recap."]
            visuals = ["Original recurring characters.", "One clear visual action for each target word.", "Readable on-screen English words.", "Simple scene changes synchronized to the song."]
        elif channel_id == "english_school":
            words = target_words or []
            titles = [f"{topic} | English Lesson", f"Learn {topic} in English", f"{topic} Explained for Students"]
            outline = ["Set a clear lesson objective.", "Explain with correct examples.", "Practice with short exercises.", "Finish with answers and recap."]
            visuals = ["Clear classroom-style graphics.", "Readable examples and captions.", "Simple diagrams where useful.", "Mobile-first subtitles."]
        else:
            words = target_words or []
            titles = [f"{topic} — An Introduction to Islam", f"What Islam Teaches About {topic}", f"{topic} Explained Clearly in English"]
            outline = ["Define the topic in plain English.", "Present primary sources and citations.", "Separate established facts from interpretation.", "Close with a concise recap and source list."]
            visuals = ["Respectful documentary-style visuals.", "On-screen source references.", "No sensationalized religious imagery.", "Clear English subtitles."]
        media_run = media_team.start_daily_run(channel_id, topic)
        plan = ChannelPlan(
            channel_id, _now()[:10], topic.strip(), titles, words, outline, visuals,
            ["trend_and_competitor_research", "source_or_lyrics_verification", "script_and_story",
             "visual_plan", "voice_and_audio", "edit_and_quality_review", "thumbnail_and_metadata",
             "publish_or_schedule", "post_publish_analytics", "learning_feedback"],
            research_signals or {}, "planned", media_run.run_id, len(media_team.agents[channel_id]))
        self.plans.append(plan)
        return plan

    def record_analytics(self, channel_id: str, video_id: str, metrics: dict[str, Any]) -> dict[str, Any]:
        self._require_channel(channel_id)
        item = {"channel_id": channel_id, "video_id": video_id, "captured_at": _now(), **metrics}
        self.analytics.append(item)
        return item

    def start_execution(self, channel_id: str, topic: str, *, dry_run: bool = True) -> dict[str, Any]:
        self._require_channel(channel_id)
        plan = self.create_daily_plan(channel_id, topic)
        event = {
            "execution_id": f"yt-{channel_id}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
            "channel_id": channel_id, "topic": topic.strip(), "dry_run": dry_run,
            "status": "ready_for_authorized_connection" if dry_run else "blocked",
            "stages": [
                "research","concept","script","fact_check","production","thumbnail",
                "metadata","quality_check","upload","publish","verify","analytics","learn"],
            "truth": "planned != executed; executed != published; published != verified",
            "reason": None if dry_run else "YouTube publishing credentials/authorized connection are not available in this layer",
            "created_at": _now(), "plan": plan.__dict__,
        }
        self.execution_events.append(event)
        return event

    def status(self) -> dict[str, Any]:
        return {
            "channels": len(CHANNELS), "plans": len(self.plans),
            "analytics_records": len(self.analytics), "research_records": len(self.research),
            "execution_records": len(self.execution_events),
            "media_team": media_team.status(),
            "publishing": "authorized_connection_required",
            "channel_urls": CHANNEL_URLS,
            "policy": "external publishing requires authorized YouTube connection and verification",
        }

    def media_status(self) -> dict[str, Any]:
        return media_team.status()

    def media_agents(self, channel_id: str) -> list[dict[str, str]]:
        self._require_channel(channel_id)
        return media_team.channel_agents(channel_id)

    def media_run(self, channel_id: str, topic: str) -> dict[str, Any]:
        self._require_channel(channel_id)
        return media_team.start_daily_run(channel_id, topic).__dict__

    def complete_media_stage(self, run_id: str, stage: str, result: dict[str, Any] | None = None) -> dict[str, Any]:
        return media_team.complete_stage(run_id, stage, result)

    def _get_channel(self, channel_id: str) -> ChannelProfile:
        if channel_id not in CHANNELS:
            raise ValueError("unknown channel")
        return CHANNELS[channel_id]

    def _require_channel(self, channel_id: str) -> None:
        self._get_channel(channel_id)

youtube_studio = YouTubeStudio()
