from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.revenue_expansion_suite import RevenueExpansionSuite

class RevenueExpansionSuiteAgent(BaseAgent):
    name = "revenue_expansion_suite_agent"
    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = RevenueExpansionSuite()
    def run(self, payload: dict) -> AgentResult:
        data = self.engine.evaluate(payload)
        if data["status"] == "evaluated":
            return AgentResult(True, data=data, next_actions=["score_opportunity", "compile_offer", "find_buyer", "measure_profit"])
        return AgentResult(False, data=data, error=data.get("reason", "validation_required"), next_actions=["collect_evidence"])
