"""Marketing Campaign Agent."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.marketing_campaign import MarketingCampaignEngine

class MarketingCampaignAgent(BaseAgent):
    name = "marketing_campaign_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = MarketingCampaignEngine()

    def run(self, payload: dict) -> AgentResult:
        result = self.engine.build(payload)
        return AgentResult(success=result["status"] == "ready", data=result, next_actions=["compile_offer", "execute_campaign"] if result["status"] == "ready" else ["collect_market_evidence"])
