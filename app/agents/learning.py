"""Evidence-first continuous learning for Hamed's five learning agents."""
from dataclasses import dataclass
from .provider import AIProvider
from .registry import LEARNING_COUNCIL

@dataclass
class KnowledgeItem:
    topic: str
    evidence: str
    confidence: str = "review"

class LearningCouncil:
    """Researches public information and produces evidence for later review.

    It never silently changes Hamed's behavior from a single web page. The
    returned material is evidence that can be stored/reviewed by the core.
    """
    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider

    def research(self, topic: str) -> KnowledgeItem:
        prompt = (
            "You are Hamed's five-agent Learning Council: psychology research, "
            "sales science, customer service research, business strategy research, "
            "and continuous learning. Research this topic using credible public "
            "sources. Prefer primary research, reputable institutions and current "
            "documentation. Separate evidence, interpretation and uncertainty. "
            "Do not diagnose people or recommend manipulative psychological tactics. "
            "Do not invent facts or citations. Return a concise evidence report with sources."
        )
        evidence = self.provider.web_research(topic, system=prompt)
        return KnowledgeItem(topic=topic, evidence=evidence, confidence="review")

    @staticmethod
    def agent_ids() -> tuple[str, ...]:
        return LEARNING_COUNCIL
