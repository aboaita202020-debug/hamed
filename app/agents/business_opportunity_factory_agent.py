"""Agent wrapper for Hamed's business opportunity factory."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.business_opportunity_factory import BusinessOpportunityFactory

class BusinessOpportunityFactoryAgent(BaseAgent):
    name = "business_opportunity_factory_agent"

    def run(self, payload: dict) -> AgentResult:
        result = BusinessOpportunityFactory().compose(payload or {})
        status = result.get("status")
        if status == "needs_input":
            return AgentResult(True, result, next_actions=["collect_opportunity_signal"])
        if status == "needs_validation":
            return AgentResult(True, result, next_actions=["collect_market_evidence", "verify_claims"])
        return AgentResult(True, result, next_actions=["score_business_models", "run_smallest_experiment", "find_first_customer", "measure_and_learn"])
