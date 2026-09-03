"""Continuous commercial learning engine for Hamed AI.

The engine ships with a structured, reusable curriculum covering sales,
purchasing, negotiation, marketing, customer intelligence and affiliate work.
It learns from evidence and observed outcomes, but it never changes safety
policies and never executes high-impact actions by itself.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class Skill(str, Enum):
    SALES = "sales"
    PURCHASING = "purchasing"
    NEGOTIATION = "negotiation"
    AFFILIATE = "affiliate_marketing"
    SERVICES = "service_sales"
    WEBSITES = "websites_and_stores"
    MARKETING = "marketing"
    CUSTOMER_INTELLIGENCE = "customer_intelligence"
    PRICING = "pricing"
    MARKET_RESEARCH = "market_research"


@dataclass
class LearningRecord:
    skill: Skill
    lesson: str
    source: str = ""
    evidence: str = ""
    outcome: str = ""
    success: Optional[bool] = None
    confidence: float = 0.5
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Baseline curriculum. These are operating principles, not permission to act.
# The model may refine them from evidence and outcomes, but safety rules remain
# higher priority than any learned strategy.
COMMERCIAL_CURRICULUM = {
    Skill.SALES: [
        "Discover the customer's goal, budget, urgency and buying criteria before pitching.",
        "Sell value and business outcome before discussing discounts.",
        "Use benefit-led product presentation tied to the customer's stated need.",
        "Handle objections by clarifying the real concern before answering it.",
        "Use social proof only when it is real and verifiable.",
        "Offer clear next steps and ask for the sale without pressure or deception.",
        "Use cross-sell and upsell only when the additional offer is genuinely relevant.",
        "Segment wholesale, retail and business buyers and adapt the offer accordingly.",
    ],
    Skill.PURCHASING: [
        "Compare total landed cost, not supplier price alone.",
        "Evaluate supplier reliability, quality, lead time, payment terms and return conditions.",
        "Request samples or inspection for material purchases when quality risk is meaningful.",
        "Use multiple supplier quotes to establish a realistic negotiation range.",
        "Separate target price, acceptable price and walk-away price before negotiating.",
        "Prefer safer payment and delivery structures when supplier risk is high.",
        "Avoid concentrating a large purchase with an unverified supplier solely because of a low price.",
        "Reorder using observed demand and inventory turnover rather than guesswork.",
    ],
    Skill.NEGOTIATION: [
        "Trade price against quantity, payment speed, delivery, warranty or other measurable value.",
        "Anchor with a reasoned offer rather than an arbitrary low number.",
        "Use silence and clarification instead of pressure or manipulation.",
        "Maintain a BATNA or credible alternative whenever possible.",
        "Never reveal confidential internal limits unless explicitly authorized.",
        "Record concessions so each concession receives a corresponding benefit.",
        "Treat a negotiated price as provisional until the authorized decision-maker approves the final deal.",
        "Escalate when the counterparty requests unusual prepayment, guarantees or irreversible commitments.",
    ],
    Skill.MARKETING: [
        "Define the ideal customer and the problem being solved before choosing a channel.",
        "Build offers around a clear value proposition and measurable outcome.",
        "Test multiple hooks and messages instead of assuming one creative will win.",
        "Use content to educate, demonstrate proof and answer objections.",
        "Measure conversion rate, customer acquisition cost, average order value and return on spend.",
        "Retarget only through lawful, consent-respecting platform capabilities.",
        "Adapt creative and language to Egypt or Gulf markets without inventing local claims.",
        "Stop or revise campaigns when evidence shows poor economics or customer harm.",
    ],
    Skill.CUSTOMER_INTELLIGENCE: [
        "Infer needs from explicit customer statements and observable conversation signals, not sensitive traits.",
        "Classify objections as price, trust, fit, timing, authority or logistics when supported by evidence.",
        "Track recurring questions to improve product pages, offers and sales scripts.",
        "Use customer feedback as evidence for product and service improvement.",
        "Never use psychological profiling to exploit vulnerabilities or pressure a customer.",
    ],
    Skill.PRICING: [
        "Calculate unit cost, landed cost, gross profit, gross margin and break-even before pricing.",
        "Keep a target price and a protected floor based on actual costs and required margin.",
        "Use quantity tiers when volume changes the economics.",
        "Do not call a negotiation floor final when taxes, freight or other costs are unknown.",
        "Compare competitor price with product quality, service and delivery rather than price alone.",
    ],
    Skill.MARKET_RESEARCH: [
        "Validate market claims against current, credible evidence when research is requested.",
        "Separate observed facts from estimates, assumptions and recommendations.",
        "Compare suppliers and products using consistent criteria.",
        "Flag stale, conflicting or insufficient market data instead of inventing certainty.",
        "Turn research into an actionable shortlist with risks and verification steps.",
    ],
    Skill.AFFILIATE: [
        "Prefer products with genuine customer fit and healthy conversion over commission alone.",
        "Disclose affiliate relationships when required by the platform or applicable rules.",
        "Track clicks, conversion rate, commission and refund rate.",
        "Avoid misleading claims, fake scarcity and fabricated reviews.",
    ],
    Skill.SERVICES: [
        "Package services around a measurable customer outcome.",
        "Define scope, deliverables, timeline and exclusions before quoting.",
        "Use tiered packages only when each tier has meaningful differentiated value.",
    ],
    Skill.WEBSITES: [
        "Optimize product and service pages for clarity, trust, proof and a single primary action.",
        "Reduce checkout friction while preserving security and accurate information.",
        "Measure page-to-lead and page-to-purchase conversion before making broad changes.",
    ],
}


class CommercialLearningEngine:
    """Stores lessons, seeds a commercial curriculum and derives playbooks."""

    def __init__(self, seed_curriculum: bool = True) -> None:
        self.records: List[LearningRecord] = []
        if seed_curriculum:
            self.seed_curriculum()

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

    def seed_curriculum(self) -> int:
        """Load the baseline commercial knowledge once per engine instance."""
        added = 0
        for skill, lessons in COMMERCIAL_CURRICULUM.items():
            for lesson in lessons:
                self.learn(LearningRecord(skill, lesson, source="built_in_curriculum", confidence=0.8))
                added += 1
        return added

    def lessons(self, skill: Optional[Skill] = None) -> List[LearningRecord]:
        if skill is None:
            return list(self.records)
        return [record for record in self.records if record.skill == skill]

    def playbook(self, skill: Skill, limit: int = 10) -> List[str]:
        records = sorted(
            self.lessons(skill),
            key=lambda r: (r.success is True, r.confidence, r.created_at),
            reverse=True,
        )
        return [r.lesson for r in records[: max(1, limit)]]

    def curriculum(self) -> Dict[str, List[str]]:
        return {skill.value: list(lessons) for skill, lessons in COMMERCIAL_CURRICULUM.items()}

    def recommend(self, skill: Skill, limit: int = 5) -> List[str]:
        """Return the strongest current lessons for a commercial task."""
        return self.playbook(skill, limit=limit)

    def summarize(self) -> Dict[str, Any]:
        return {
            "total_lessons": len(self.records),
            "curriculum_lessons": sum(len(v) for v in COMMERCIAL_CURRICULUM.values()),
            "skills": len(COMMERCIAL_CURRICULUM),
            "by_skill": {
                skill.value: len(self.lessons(skill)) for skill in Skill if self.lessons(skill)
            },
            "successful_outcomes": sum(r.success is True for r in self.records),
            "failed_outcomes": sum(r.success is False for r in self.records),
        }
