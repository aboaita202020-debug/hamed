"""Agent wrapper for Hamed's business asset/network/meta-opportunity engine."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.business_asset_network_engine import BusinessAssetNetworkEngine

class BusinessAssetNetworkAgent(BaseAgent):
    name = "business_asset_network_agent"
    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = BusinessAssetNetworkEngine()
    def run(self, payload: dict) -> AgentResult:
        if payload.get("catalog"):
            return AgentResult(success=True, data=self.engine.catalog())
        return AgentResult(success=True, data=self.engine.evaluate(payload))
