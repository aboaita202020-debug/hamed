"""Autonomous content-channel operating configuration for Hamed AGI."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class ChannelTeam:
    key: str
    name: str
    niche: str
    assistant_count: int = 100
    daily_long_videos: int = 1
    short_reels_per_video: int = 1
    publish_strategy: str = "analytics_optimized"
    ai_disclosure_policy: str = "official_youtube_disclosure_when_required"
    autonomous: bool = True


CHANNELS: dict[str, ChannelTeam] = {
    "lumilkids": ChannelTeam(
        key="lumilkids",
        name="LumiKids",
        niche="children songs, stories and educational entertainment",
    ),
    "english_songs": ChannelTeam(
        key="english_songs",
        name="English Learning Songs",
        niche="English learning through original songs",
    ),
}


def channel_plan(channel_key: str) -> dict[str, Any]:
    team = CHANNELS[channel_key]
    return {
        **asdict(team),
        "workflow": [
            "trend_research",
            "competitor_video_analysis",
            "opportunity_selection",
            "original_content_creation",
            "quality_and_policy_review",
            "daily_publish",
            "short_or_reel_publish",
            "analytics_review",
            "learning_and_next_topic",
        ],
        "publish_time": {
            "strategy": "learn_from_channel_analytics",
            "fixed_time": None,
            "timezone": "channel_audience_local",
        },
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def all_channel_plans() -> list[dict[str, Any]]:
    return [channel_plan(k) for k in CHANNELS]


def channel_status() -> dict[str, Any]:
    return {
        "status": "ok",
        "channels": all_channel_plans(),
        "total_dedicated_assistants": sum(c.assistant_count for c in CHANNELS.values()),
        "daily_long_videos": sum(c.daily_long_videos for c in CHANNELS.values()),
        "daily_shorts_or_reels_minimum": sum(
            c.daily_long_videos * c.short_reels_per_video for c in CHANNELS.values()
        ),
        "execution": "autonomous",
    }
