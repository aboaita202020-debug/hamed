from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Any

from .agent_bus import agent_bus
from .memory_store import memory_store
from .universal_learning import universal_learning

CAIRO = ZoneInfo("Africa/Cairo")
REPORT_HOUR = 19
REPORT_MINUTE = 50
IMPROVEMENT_MINUTES = 10

class DailyLearningCycle:
    """Coordinates the daily team report and the immediate improvement sprint."""
    def __init__(self) -> None:
        self.last_report: dict[str, Any] | None = None
        self.last_improvement: dict[str, Any] | None = None

    def report(self, now: datetime | None = None) -> dict[str, Any]:
        now = (now or datetime.now(CAIRO)).astimezone(CAIRO)
        report = {
            "type": "daily_learning_report",
            "generated_at": now.isoformat(),
            "timezone": "Africa/Cairo",
            "scheduled_time": "19:50",
            "team": "all_agents",
            "learning": universal_learning.status(),
            "memory_entries": len(memory_store.recent(500)),
            "messages": agent_bus.status()["messages"],
            "next_step": "start_improvement_sprint_immediately",
        }
        memory_store.record("daily_learning_report", report, source="daily_learning_cycle")
        self.last_report = report
        return report

    def improvement(self, now: datetime | None = None) -> dict[str, Any]:
        now = (now or datetime.now(CAIRO)).astimezone(CAIRO)
        started = now
        finished = started + timedelta(minutes=IMPROVEMENT_MINUTES)
        result = {
            "type": "daily_improvement_sprint",
            "started_at": started.isoformat(),
            "scheduled_after": "19:50 daily report",
            "duration_minutes": IMPROVEMENT_MINUTES,
            "ends_at": finished.isoformat(),
            "steps": ["review_errors", "identify_causes", "propose_changes", "test_changes", "store_lessons"],
            "safety": "tests_and_governance_required_before_promotion",
        }
        memory_store.record("daily_improvement_sprint", result, source="daily_learning_cycle")
        self.last_improvement = result
        return result

    def run(self, now: datetime | None = None) -> dict[str, Any]:
        report = self.report(now)
        improvement = self.improvement(now)
        return {"status": "completed", "report": report, "improvement": improvement}

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "timezone": "Africa/Cairo",
            "daily_report": "19:50",
            "improvement_after_report_minutes": IMPROVEMENT_MINUTES,
            "last_report": self.last_report,
            "last_improvement": self.last_improvement,
        }

daily_learning_cycle = DailyLearningCycle()
