"""Agent wrapper for revenue infrastructure capabilities."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.revenue_infrastructure_suite import RevenueInfrastructureSuite

class RevenueInfrastructureSuiteAgent(BaseAgent):
    name = "revenue_infrastructure_suite_agent"
    def run(self, payload: dict) -> AgentResult:
        result = RevenueInfrastructureSuite().evaluate(payload or {})
        if result["status"] == "needs_input":
            return AgentResult(True, result, next_actions=["collect_signal"])
        if result["status"] == "needs_validation":
            return AgentResult(True, result, next_actions=["collect_market_evidence", "verify_claims"])
        return AgentResult(True, result, next_actions=["score_capabilities", "run_small_test", "measure_revenue", "scale_or_kill"])
