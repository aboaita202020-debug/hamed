"""Research -> learn -> verify -> apply loop for Hamed."""
from __future__ import annotations

from typing import Any

from .source_connectors import SourceRegistry


class LearningLoop:
    def __init__(self, registry: SourceRegistry, learner: Any) -> None:
        self.registry = registry
        self.learner = learner

    def run(self, topic: str, limit_per_source: int = 5) -> dict[str, Any]:
        sources = self.registry.search_all(topic, limit_per_source)
        lessons = []
        for source in sources:
            try:
                result = self.learner.learn_from_source(source)
                lessons.append(result)
            except Exception as exc:
                lessons.append({"source": source.uri, "status": "failed", "error": str(exc)})
        return {
            "topic": topic,
            "sources_found": len(sources),
            "lessons": lessons,
            "next": "verify_then_build_playbook",
        }
