"""Evidence-first continuous learning for Hamed's learning council."""
from dataclasses import dataclass
from typing import Optional

from .provider import AIProvider
from .registry import LEARNING_COUNCIL
from .learning_engine import CommercialLearningEngine, LearningRecord, Skill


@dataclass
class KnowledgeItem:
    topic: str
    evidence: str
    confidence: str = "review"


class LearningCouncil:
    """Combines researched evidence with a structured commercial curriculum.

    Research is evidence for review; it does not silently override safety rules.
    Commercial lessons can be reinforced by observed outcomes, but high-impact
    actions remain subject to the approval layer.
    """

    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider
        self.commercial = CommercialLearningEngine()

    def research(self, topic: str) -> KnowledgeItem:
        prompt = (
            "You are Hamed's learning council. Research this topic using credible "
            "public sources. Prefer primary research, reputable institutions and "
            "current documentation. Separate evidence, interpretation and uncertainty. "
            "For sales, purchasing, negotiation and marketing, extract practical "
            "strategies, assumptions, risks and measurable KPIs. Do not diagnose people "
            "or recommend manipulative psychological tactics. Do not invent facts or citations. "
            "Return a concise evidence report with sources."
        )
        evidence = self.provider.web_research(topic, system=prompt)
        return KnowledgeItem(topic=topic, evidence=evidence, confidence="review")

    def commercial_playbook(self, skill: str, limit: int = 10):
        """Return the current playbook for a commercial skill."""
        try:
            selected = Skill(skill)
        except ValueError:
            selected = Skill.SALES
        return self.commercial.recommend(selected, limit=limit)

    def record_outcome(self, skill: str, lesson: str, outcome: str, success: bool):
        """Learn from an observed result without changing safety permissions."""
        return self.commercial.learn_from_outcome(Skill(skill), lesson, outcome, success)

    def commercial_summary(self):
        return self.commercial.summarize()

    @staticmethod
    def agent_ids() -> tuple[str, ...]:
        return LEARNING_COUNCIL
