from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from .agent_bus import agent_bus
from .memory_store import memory_store

SOURCE_FAMILIES = (
    "web", "research", "universities", "youtube", "books", "github",
    "business_leaders", "official_docs", "market_data", "communities",
    "experiments", "public_datasets", "courses", "podcasts", "news",
)

@dataclass(frozen=True)
class LearningSource:
    name: str
    family: str
    priority: int
    access: str = "public_or_authorized"
    verification: str = "cross_source"

@dataclass
class KnowledgePackage:
    topic: str
    source: str
    family: str
    claim: str
    evidence_type: str
    confidence: float
    verified: bool
    collected_at: str
    references: list[str]
    notes: str = ""

class UniversalLearningEngine:
    """Source-agnostic learning registry. It plans discovery, verification and teaching;
    it does not bypass access controls or use exposed credentials."""

    def __init__(self) -> None:
        self.sources = [
            LearningSource("Web", "web", 70),
            LearningSource("Scientific research", "research", 95),
            LearningSource("Universities & research centers", "universities", 100),
            LearningSource("YouTube", "youtube", 65),
            LearningSource("Books & references", "books", 90),
            LearningSource("GitHub & open source", "github", 90),
            LearningSource("Business leaders & entrepreneurs", "business_leaders", 75),
            LearningSource("Official documentation", "official_docs", 100),
            LearningSource("Market & public data", "market_data", 85),
            LearningSource("Public communities", "communities", 45),
            LearningSource("Experiments & benchmarks", "experiments", 100),
            LearningSource("Public datasets", "public_datasets", 80),
            LearningSource("Courses", "courses", 60),
            LearningSource("Podcasts", "podcasts", 55),
            LearningSource("News", "news", 50),
        ]
        self.packages: list[KnowledgePackage] = []

    def source_catalog(self) -> list[dict[str, Any]]:
        return [asdict(s) for s in self.sources]

    def create_learning_plan(self, topic: str) -> dict[str, Any]:
        topic = topic.strip()
        if not topic:
            raise ValueError("topic is required")
        ordered = sorted(self.sources, key=lambda s: (-s.priority, s.family))
        return {
            "topic": topic,
            "pipeline": ["discover", "collect", "extract", "cross_check",
                         "experiment", "peer_review", "promote", "teach", "monitor"],
            "sources": [asdict(s) for s in ordered],
            "safety": [
                "public_or_authorized_access_only",
                "never_use_leaked_credentials",
                "respect_source_terms_and_rate_limits",
                "do_not_copy_protected_content_as_training_data",
            ],
        }

    def record_knowledge(
        self, topic: str, source: str, family: str, claim: str,
        evidence_type: str = "secondary", confidence: float = 0.5,
        verified: bool = False, references: list[str] | None = None,
        notes: str = ""
    ) -> dict[str, Any]:
        confidence = max(0.0, min(1.0, float(confidence)))
        package = KnowledgePackage(
            topic=topic, source=source, family=family, claim=claim,
            evidence_type=evidence_type, confidence=confidence,
            verified=verified,
            collected_at=datetime.now(timezone.utc).isoformat(),
            references=references or [], notes=notes,
        )
        self.packages.append(package)
        item = asdict(package)
        memory_store.record("knowledge_package", item, source=source)
        return item

    def verify(self, package: dict[str, Any], supporting_sources: int = 0,
               has_primary_evidence: bool = False,
               experimentally_tested: bool = False) -> dict[str, Any]:
        score = float(package.get("confidence", 0.0))
        if supporting_sources >= 2:
            score += 0.10
        if has_primary_evidence:
            score += 0.15
        if experimentally_tested:
            score += 0.20
        verified = score >= 0.75 and (has_primary_evidence or supporting_sources >= 2 or experimentally_tested)
        result = {**package, "confidence": min(score, 1.0), "verified": verified}
        if verified:
            agent_bus.broadcast("universal_learning", "LEARN",
                                {"topic": package.get("topic"), "knowledge": result},
                                ["learning"])
        return result

    def teach_network(self, package: dict[str, Any], agent_names: list[str]) -> dict[str, Any]:
        if not package.get("verified"):
            return {"status": "blocked", "reason": "knowledge_not_verified"}
        messages = agent_bus.broadcast(
            "universal_learning", "LEARN",
            {"knowledge": package, "instruction": "apply_and_report_results"},
            agent_names,
        )
        return {"status": "taught", "recipients": len(messages)}

    def status(self) -> dict[str, Any]:
        return {
            "engine": "Universal Learning Engine",
            "source_families": len(SOURCE_FAMILIES),
            "registered_sources": len(self.sources),
            "knowledge_packages": len(self.packages),
            "mode": "continuous_discovery_verification_learning",
        }

universal_learning = UniversalLearningEngine()
