"""Evidence-first continuous learning for Hamed's learning council."""
from dataclasses import dataclass
from typing import Tuple

from .provider import AIProvider
from .registry import LEARNING_COUNCIL
from .learning_engine import CommercialLearningEngine, LearningRecord, Skill
from .multimedia_learning import MultimediaLearningEngine


@dataclass
class KnowledgeItem:
    topic: str
    evidence: str
    confidence: str = "review"


class LearningCouncil:
    """Combines web/video/document research with a reusable commercial curriculum."""

    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider
        self.commercial = CommercialLearningEngine()
        self.multimedia = MultimediaLearningEngine(self.commercial)

    def research(self, topic: str) -> KnowledgeItem:
        prompt = (
            "You are Hamed's learning council. Research this topic using credible public sources. "
            "Search broadly across reputable articles, academic research, industry reports, "
            "books/courses and public educational videos or interviews. When a video has a "
            "public transcript or reliable summary, extract its useful teaching points; never "
            "pretend to have watched a video when only metadata is available. Prefer primary "
            "research and reputable practitioners. Separate evidence, interpretation and uncertainty. "
            "For sales, marketing and customer psychology, extract practical discovery questions, "
            "buyer signals, objections, value framing, negotiation patterns, message examples and KPIs. "
            "Use psychology to understand observable behavior, not to diagnose, manipulate or exploit. "
            "Return a concise evidence report with source titles/URLs when available. Do not invent facts or citations."
        )
        evidence = self.provider.web_research(topic, system=prompt)
        return KnowledgeItem(topic=topic, evidence=evidence, confidence="review")

    def study(self, topic: str = "sales, marketing and customer psychology") -> KnowledgeItem:
        """Run a broad multimedia learning pass and store the evidence as a lesson."""
        plan = self.multimedia.build_research_plan(topic)
        item = self.research(" ; ".join(plan))
        skill = self.multimedia._skill_for_topic(topic)
        self.commercial.learn(LearningRecord(
            skill=skill,
            lesson=(
                "Use evidence-backed customer discovery and sales strategy learned from a broad "
                "multimedia research pass; adapt to the customer's explicit need and verify current facts."
            ),
            source="continuous_multimedia_web_research",
            evidence=item.evidence,
            confidence=0.65,
        ))
        return item

    def commercial_playbook(self, skill: str, limit: int = 10):
        try:
            selected = Skill(skill)
        except ValueError:
            selected = Skill.SALES
        return self.commercial.recommend(selected, limit=limit)

    def record_outcome(self, skill: str, lesson: str, outcome: str, success: bool):
        return self.commercial.learn_from_outcome(Skill(skill), lesson, outcome, success)

    def commercial_summary(self):
        summary = self.commercial.summarize()
        summary["multimedia"] = self.multimedia.summary()
        return summary

    @staticmethod
    def agent_ids() -> Tuple[str, ...]:
        return LEARNING_COUNCIL
