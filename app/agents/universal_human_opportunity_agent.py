"""Agent wrapper for universal human opportunity discovery and routing."""
from __future__ import annotations
from app.services.universal_human_opportunity import UniversalHumanOpportunityEngine
from .base_agent import BaseAgent, AgentResult


class UniversalHumanOpportunityAgent(BaseAgent):
    name = "universal_human_opportunity_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = UniversalHumanOpportunityEngine()

    def run(self, payload: dict) -> AgentResult:
        result = self.engine.evaluate(payload)
        opportunity = result["opportunity"]
        if opportunity["status"] == "opted_out":
            return AgentResult(success=True, data=result)
        return AgentResult(success=True, data=result)
