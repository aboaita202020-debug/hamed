"""Freelance Revenue Agent."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.freelance_revenue import FreelanceRevenueEngine

class FreelanceRevenueAgent(BaseAgent):
    name = "freelance_revenue_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = FreelanceRevenueEngine()

    def run(self, payload: dict) -> AgentResult:
        result = self.engine.qualify(payload)
        return AgentResult(success=result["status"] == "qualified", data=result, next_actions=result.get("opportunity", {}).get("next_actions", ["collect_project_evidence"]))
