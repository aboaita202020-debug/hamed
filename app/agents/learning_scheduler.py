"""Scheduled learning coordinator.

This module defines what Hamed should learn and how knowledge is routed to
specialists. Actual fetching must use configured, lawful connectors/tools.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .continuous_learning import ContinuousLearning, KnowledgeItem
from .team import AgentTeam


@dataclass(frozen=True)
class LearningTarget:
    topic: str
    source_types: tuple[str, ...]
    objective: str


DEFAULT_TARGETS = (
    LearningTarget("sales", ("book", "expert_interview", "entrepreneur_case", "academic", "community"), "improve qualification and closing"),
    LearningTarget("negotiation", ("book", "entrepreneur_case", "expert_interview", "community"), "improve value-based negotiation"),
    LearningTarget("marketing", ("book", "market_report", "entrepreneur_case", "news"), "improve acquisition and conversion"),
    LearningTarget("websites", ("official_docs", "book", "academic", "entrepreneur_case"), "improve delivery quality"),
    LearningTarget("ecommerce", ("official_docs", "market_report", "entrepreneur_case", "community"), "improve store execution"),
    LearningTarget("finance", ("academic", "market_report", "official_docs", "entrepreneur_case"), "improve unit economics"),
    LearningTarget("engineering", ("official_docs", "academic", "book", "observed_outcome"), "improve engineering reliability"),
    LearningTarget("operations", ("book", "entrepreneur_case", "observed_outcome"), "improve execution workflows"),
)


class LearningCoordinator:
    def __init__(self, learner: ContinuousLearning | None = None, team: AgentTeam | None = None) -> None:
        self.learner = learner or ContinuousLearning()
        self.team = team or AgentTeam()
        self.targets = list(DEFAULT_TARGETS)

    def add_target(self, topic: str, source_types: tuple[str, ...], objective: str) -> None:
        self.targets.append(LearningTarget(topic, source_types, objective))

    def ingest_verified_material(self, topic: str, source: str, source_type: str,
                                 lessons: list[str], actions: list[str], claims: list[str] | None = None,
                                 confidence: float = 0.7, verified_by: list[str] | None = None) -> KnowledgeItem:
        item = KnowledgeItem(topic=topic, source=source, source_type=source_type,
                             claims=claims or [], lessons=lessons, actions=actions,
                             confidence=confidence, verified_by=verified_by or [])
        return self.learner.ingest(item)

    def build_learning_cycle(self) -> list[dict[str, Any]]:
        return [{"topic": t.topic, "source_types": list(t.source_types), "objective": t.objective,
                 "delegated_to": [a.key for a in self.team.select(t.topic, limit=3)]} for t in self.targets]

    def apply_knowledge_to_team(self, topic: str) -> dict[str, Any]:
        playbook = self.learner.extract_playbook(topic)
        agents = [a.key for a in self.team.select(topic, limit=5)]
        return {"topic": topic, "playbook": playbook, "agents": agents}
