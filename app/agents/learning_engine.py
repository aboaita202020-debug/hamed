"""Continuous commercial learning primitives for Hamed AI.

Learns from legally accessible evidence and observed outcomes without changing
security policies or executing high-impact actions.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Skill(str, Enum):
    SALES = "sales"
    PURCHASING = "purchasing"
    NEGOTIATION = "negotiation"
    AFFILIATE = "affiliate_marketing"
    SERVICES = "service_sales"
    WEBSITES = "websites_and_stores"
    MARKETING = "marketing"


@dataclass
class LearningRecord:
    skill: Skill
    lesson: str
    source: str = ""
    evidence: str = ""
    outcome: str = ""
    success: bool | None = None
    confidence: float = 0.5
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CommercialLearningEngine:
    """Stores lessons, scores evidence, and derives repeatable playbooks."""

    def __init__(self) -> None:
        self.records: list[LearningRecord] = []

    def learn(self, record: LearningRecord) -> LearningRecord:
        record.confidence = max(0.0, min(1.0, record.confidence))
        self.records.append(record)
        return record

    def learn_from_outcome(
        self,
        skill: Skill,
        lesson: str,
        outcome: str,
        success: bool,
        source: str = "observed_outcome",
    ) -> LearningRecord:
        confidence = 0.7 if success else 0.3
        return self.learn(LearningRecord(skill, lesson, source, outcome, outcome, success, confidence))

    def lessons(self, skill: Skill | None = None) -> list[LearningRecord]:
        if skill is None:
            return list(self.records)
        return [record for record in self.records if record.skill == skill]

    def playbook(self, skill: Skill, limit: int = 10) -> list[str]:
        records = sorted(
            self.lessons(skill),
            key=lambda r: (r.success is True, r.confidence, r.created_at),
            reverse=True,
        )
        return [r.lesson for r in records[: max(1, limit)]]

    def summarize(self) -> dict[str, Any]:
        return {
            "total_lessons": len(self.records),
            "by_skill": {
                skill.value: len(self.lessons(skill)) for skill in Skill if self.lessons(skill)
            },
            "successful_outcomes": sum(r.success is True for r in self.records),
            "failed_outcomes": sum(r.success is False for r in self.records),
        }
