"""Agent wrapper for deep website/e-commerce intelligence."""
from __future__ import annotations
from app.services.website_ecommerce_intelligence import WebsiteEcommerceIntelligence
from .base_agent import BaseAgent, AgentResult


class WebsiteEcommerceIntelligenceAgent(BaseAgent):
    name = "website_ecommerce_intelligence_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = WebsiteEcommerceIntelligence()

    def run(self, payload: dict) -> AgentResult:
        result = self.engine.evaluate(payload)
        if not result["success"]:
            return AgentResult(success=False, error="website_target_required", data=result)
        return AgentResult(success=True, data=result)
