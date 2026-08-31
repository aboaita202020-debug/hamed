"""Continuous knowledge acquisition pipeline for Hamed AI.

Sources are classified by provenance and reliability. The pipeline produces
structured knowledge for the agent team; it does not grant new permissions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


SOURCE_POLICIES = {
    "official_docs": 0.95,
    "academic": 0.90,
    "book": 0.85,
    "expert_interview": 0.75,
    "entrepreneur_case": 0.75,
    "market_report": 0.80,
    "news": 0.65,
    "community": 0.45,
    "user_review": 0.40,
    "observed_outcome": 0.90,
}


@dataclass
class KnowledgeItem:
    topic: str
    source: str
    source_type: str
    claims: list[str] = field(default_factory=list)
    lessons: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    confidence: float = 0.5
    verified_by: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ContinuousLearning:
    def __init__(self) -> None:
        self.items: list[KnowledgeItem] = []

    def ingest(self, item: KnowledgeItem) -> KnowledgeItem:
        baseline = SOURCE_POLICIES.get(item.source_type, 0.30)
        item.confidence = max(0.0, min(1.0, min(item.confidence, baseline) if item.confidence else baseline))
        self.items.append(item)
        return item

    def verify(self, item: KnowledgeItem, independent_sources: list[str]) -> KnowledgeItem:
        item.verified_by.extend(x for x in independent_sources if x not in item.verified_by)
        if len(item.verified_by) >= 2:
            item.confidence = min(0.98, item.confidence + 0.15)
        return item

    def extract_playbook(self, topic: str, minimum_confidence: float = 0.65) -> dict[str, Any]:
        relevant = [i for i in self.items if i.topic.lower() == topic.lower() and i.confidence >= minimum_confidence]
        lessons, actions = [], []
        for item in relevant:
            lessons.extend(x for x in item.lessons if x not in lessons)
            actions.extend(x for x in item.actions if x not in actions)
        return {"topic": topic, "sources": [i.source for i in relevant], "lessons": lessons,
                "actions": actions, "confidence": max((i.confidence for i in relevant), default=0.0)}

    def entrepreneur_pattern(self, topic: str, cases: list[KnowledgeItem]) -> dict[str, Any]:
        """Compare entrepreneur cases and return recurring patterns, not copied text."""
        relevant = [c for c in cases if c.source_type == "entrepreneur_case" and c.topic.lower() == topic.lower()]
        patterns: list[str] = []
        for case in relevant:
            for lesson in case.lessons:
                if lesson not in patterns:
                    patterns.append(lesson)
        return {"topic": topic, "cases": len(relevant), "patterns": patterns}

    def status(self) -> dict[str, Any]:
        return {"items": len(self.items), "source_types": sorted({i.source_type for i in self.items}),
                "high_confidence": sum(i.confidence >= 0.8 for i in self.items)}
