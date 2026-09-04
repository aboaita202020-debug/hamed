"""Continuous evidence learning from web pages, public video transcripts and documents.

This module does not claim to watch every video on the internet. It discovers
relevant public learning material, extracts/uses available text or transcripts,
turns it into evidence-backed lessons, and stores source metadata for later
review. Safety and platform terms remain higher priority than learned tactics.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .learning_engine import CommercialLearningEngine, LearningRecord, Skill


@dataclass
class LearningSource:
    title: str
    url: str
    source_type: str
    topic: str
    evidence: str = ""
    quality: float = 0.5
    captured_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class MultimediaLearningEngine:
    """Builds an evidence-first learning corpus for commercial skills."""

    TOPICS = (
        "sales discovery and consultative selling",
        "customer psychology and buyer behavior",
        "objection handling and negotiation",
        "marketing strategy and conversion optimization",
        "B2B and B2C customer acquisition",
        "pricing, value communication and offer design",
        "digital services, websites and ecommerce sales",
        "Egypt and Gulf customer behavior and commercial practices",
    )

    def __init__(self, commercial=None):
        self.commercial = commercial or CommercialLearningEngine()
        self.sources = []

    def build_research_plan(self, topic=None):
        selected = topic or "sales, marketing and customer psychology"
        return [
            f"{selected} peer reviewed research and university material",
            f"{selected} current industry reports and reputable practitioner material",
            f"{selected} YouTube interviews, lectures and training videos with public transcripts",
            f"{selected} books, courses and long-form educational material",
            f"{selected} real-world case studies and customer objections",
            f"{selected} Egypt and Gulf market examples",
        ]

    def ingest(self, *, title, url, source_type, topic, evidence, quality=0.5):
        source = LearningSource(title, url, source_type, topic, evidence,
                                max(0.0, min(1.0, quality)))
        self.sources.append(source)
        return source

    def convert_evidence_to_lessons(self, source):
        if not source.evidence.strip():
            return []
        skill = self._skill_for_topic(source.topic)
        lesson = (
            f"Evidence from {source.source_type}: {source.title}. "
            "Use the extracted evidence to improve discovery, value communication, "
            "objection handling or customer understanding; verify before treating it as fact."
        )
        return [LearningRecord(skill=skill, lesson=lesson, source=source.url,
                               evidence=source.evidence, confidence=source.quality)]

    def add_verified_lesson(self, *, skill, lesson, source, evidence, confidence=0.7):
        if not evidence.strip():
            raise ValueError("evidence is required")
        return self.commercial.learn(LearningRecord(
            skill=skill, lesson=lesson, source=source, evidence=evidence,
            confidence=confidence,
        ))

    @staticmethod
    def _skill_for_topic(topic):
        t = topic.lower()
        if "psychology" in t or "buyer" in t or "customer" in t:
            return Skill.CUSTOMER_INTELLIGENCE
        if "marketing" in t or "conversion" in t:
            return Skill.MARKETING
        if "negotiat" in t or "objection" in t:
            return Skill.NEGOTIATION
        if "pricing" in t:
            return Skill.PRICING
        if "website" in t or "ecommerce" in t or "digital" in t:
            return Skill.WEBSITES
        return Skill.SALES

    def summary(self):
        return {
            "sources": len(self.sources),
            "topics": list(self.TOPICS),
            "research_plan": self.build_research_plan(),
            "commercial_learning": self.commercial.summarize(),
        }
