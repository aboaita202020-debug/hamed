from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.economic_intelligence_engine import EconomicIntelligenceEngine

class EconomicIntelligenceAgent(BaseAgent):
    name = "economic_intelligence_agent"
    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = EconomicIntelligenceEngine()
    def run(self, payload: dict) -> AgentResult:
        try:
            if payload.get("action") == "catalog":
                return AgentResult(success=True, data=self.engine.catalog())
            if payload.get("action") == "invent":
                return AgentResult(success=True, data=self.engine.invent(payload))
            return AgentResult(success=True, data=self.engine.evaluate(payload))
        except Exception as exc:
            return AgentResult(success=False, error=str(exc))
