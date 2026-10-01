"""OpportunityHunterAgent — spec section 6.

Turns raw signals (from web_search or any social/business intel adapter)
into scored Opportunity records. Never invents a company or a fact: if
web_search returns NO_PROVIDER_CONFIGURED, it reports that plainly
instead of pretending to have found leads (spec section 28).
"""
from __future__ import annotations

from app.db.models import Opportunity
from .base_agent import BaseAgent, AgentResult


def score_opportunity(confidence: float, potential_value: float) -> float:
    """Simple, transparent scoring: confidence (0-1) weighted by value.
    Kept intentionally simple and explainable; replace with a learned
    model later without changing the Agent's interface."""
    normalized_value = min(potential_value / 10000.0, 1.0)  # cap influence
    return round((0.6 * confidence + 0.4 * normalized_value) * 100, 2)


class OpportunityHunterAgent(BaseAgent):
    name = "opportunity_hunter"

    def run(self, payload: dict) -> AgentResult:
        """payload: {"query": str, "opp_type": str, "lead_id": Optional[int]}"""
        query = payload.get("query", "")
        opp_type = payload.get("opp_type", "general")
        lead_id = payload.get("lead_id")

        result = self.tools.execute(actor=self.name, tool_name="web_search", query=query)
        if not result.success:
            return AgentResult(success=False, error=result.error,
                                next_actions=["configure_web_search_provider"])

        opportunities = []
        for item in result.data:
            confidence = item.get("confidence", 0.5)
            potential_value = payload.get("assumed_value", 5000.0)
            opp = Opportunity(
                lead_id=lead_id,
                source=item.get("source", "web"),
                opp_type=opp_type,
                confidence=confidence,
                opportunity_score=score_opportunity(confidence, potential_value),
                potential_value=potential_value,
                next_step="research_and_qualify",
            )
            opportunities.append(self.repo.add_opportunity(opp))

        return AgentResult(
            success=True,
            data=opportunities,
            next_actions=["lead_research"] if opportunities else [],
        )
