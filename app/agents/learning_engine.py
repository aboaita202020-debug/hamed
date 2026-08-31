"""Learning from books and community knowledge.

Hamed converts legally accessible or user-provided material into structured
lessons and practical playbooks. Source provenance is retained, and external
content never changes authorization or security policies.
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
    RESEARCH = "research"
    OPERATIONS = "operations"
    FINANCE = "finance"
    ENGINEERING = "engineering"


@dataclass
class LearningRecord:
    skill: Skill
    lesson: str
    source: str = ""
    evidence: str = ""
    outcome: str = ""
    success: bool | None = None
    confidence: float = 0.5
    source_type: str = "outcome"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class BookUnderstanding:
    source_id: str
    title: str
    summary: str
    concepts: list[str] = field(default_factory=list)
    principles: list[str] = field(default_factory=list)
    procedures: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    provenance: str = ""


class CommercialLearningEngine:
    """Stores lessons, understands source material, and derives playbooks."""

    def __init__(self) -> None:
        self.records: list[LearningRecord] = []
        self.sources: dict[str, BookUnderstanding] = {}

    def learn(self, record: LearningRecord) -> LearningRecord:
        record.confidence = max(0.0, min(1.0, record.confidence))
        self.records.append(record)
        return record

    def ingest_book(self, source_id: str, title: str, summary: str, concepts: list[str],
                    principles: list[str], procedures: list[str], examples: list[str] | None = None,
                    limitations: list[str] | None = None, provenance: str = "") -> BookUnderstanding:
        """Register a structured understanding produced from an accessible/user-provided book."""
        understanding = BookUnderstanding(source_id, title, summary, concepts, principles, procedures,
                                          examples or [], limitations or [], provenance)
        self.sources[source_id] = understanding
        return understanding

    def build_playbook(self, source_id: str) -> dict[str, Any]:
        """Turn a book's principles into an original, testable operating playbook."""
        source = self.sources[source_id]
        return {
            "source": source.title,
            "summary": source.summary,
            "principles": source.principles,
            "procedures": source.procedures,
            "experiments": ["apply on a small reversible task", "measure outcome", "compare against baseline"],
            "limitations": source.limitations,
            "provenance": source.provenance,
        }

    def learn_from_community(self, community: str, discussion: str, lessons: list[str],
                             evidence: str = "") -> list[LearningRecord]:
        """Learn patterns from permitted community discussions without treating opinions as facts."""
        return [self.learn(LearningRecord(Skill.RESEARCH, lesson, community, evidence,
                                          source_type="community", confidence=0.35)) for lesson in lessons]

    def learn_from_outcome(self, skill: Skill, lesson: str, outcome: str, success: bool,
                           source: str = "observed_outcome") -> LearningRecord:
        confidence = 0.7 if success else 0.3
        return self.learn(LearningRecord(skill, lesson, source, outcome, outcome, success, confidence, "outcome"))

    def lessons(self, skill: Skill | None = None) -> list[LearningRecord]:
        if skill is None:
            return list(self.records)
        return [record for record in self.records if record.skill == skill]

    def playbook(self, skill: Skill, limit: int = 10) -> list[str]:
        records = sorted(self.lessons(skill), key=lambda r: (r.success is True, r.confidence, r.created_at), reverse=True)
        return [r.lesson for r in records[: max(1, limit)]]

    def summarize(self) -> dict[str, Any]:
        return {
            "total_lessons": len(self.records),
            "sources": len(self.sources),
            "by_skill": {skill.value: len(self.lessons(skill)) for skill in Skill if self.lessons(skill)},
            "successful_outcomes": sum(r.success is True for r in self.records),
            "failed_outcomes": sum(r.success is False for r in self.records),
        }
