from __future__ import annotations

from .config import settings
from .learning import memory
from .models import Mission, Offer, Opportunity
from .opportunity import OpportunityEngine
from .orchestrator import orchestrator
from .providers import openai_provider


class AGIEngine:
    def __init__(self) -> None:
        self.opportunities = OpportunityEngine(settings.min_opportunity_score)

    def analyze(self, opportunity: Opportunity) -> Opportunity:
        if not opportunity.evidence:
            opportunity.evidence = ["Evidence must be collected before a factual claim is sent to a prospect."]
        return opportunity

    def create_offer(self, opportunity: Opportunity, prospect_name: str = "صاحب المتجر") -> Offer:
        return Offer(
            subject="ملاحظة سريعة على المتجر",
            message=(f"أهلًا {prospect_name}، راجعت نقطة محددة في تجربة المتجر: {opportunity.problem} نقدر نبدأ بتدقيق سريع ونقيس الأثر قبل أي تغيير كبير. لو مناسب، أرسل لك ملخصًا عمليًا وخطة أولية."),
            service=opportunity.solution,
            next_step="مراجعة قصيرة ثم اقتراح تجربة قابلة للقياس",
            evidence=opportunity.evidence,
        )

    def run(self, objective: str) -> Mission:
        mission = Mission(objective=objective, status="running")
        opportunities = [self.analyze(x) for x in self.opportunities.discover(mission)]
        mission.opportunities = opportunities
        mission.offers = [self.create_offer(x) for x in opportunities]
        mission.actions = [
            "discover", "research", "analyze", "generate_strategy",
            "draft_personalized_offer", "measure", "learn",
        ]

        # Real model reasoning is advisory only: no outreach, purchase, payment,
        # or irreversible action is performed by this mission.
        try:
            model_result = openai_provider.generate(
                "You are ORVIA AGI's commercial strategy analyst. "
                "Do not contact anyone or execute transactions. "
                f"Evaluate and rank these sandbox opportunities for this objective: {objective}. "
                f"Opportunities: {[x.model_dump() for x in opportunities]}. "
                "Return concise reasoning, key risks, and the safest next experiment."
            )
        except Exception as exc:
            from .providers import ModelResult
            model_result = ModelResult(
                text=f"SAFE_FALLBACK: external model unavailable ({type(exc).__name__}). Mission continued without external execution.",
                model="offline-fallback",
                connected=False,
            )
        mission.metadata["model"] = model_result.model
        mission.metadata["model_connected"] = model_result.connected
        mission.metadata["strategy_analysis"] = model_result.text
        mission.metadata["financial_actions"] = "blocked_by_approval_gate"
        mission.metadata["outreach"] = "disabled_for_test"
        mission.metadata["agents"] = orchestrator.run(objective)
        memory.record(
            topic="mission",
            lesson=f"Sandbox mission completed for: {objective}",
            source="orvia_agi_mission",
            confidence=0.80,
        )
        mission.status = "completed"
        return mission

agi_engine = AGIEngine()
