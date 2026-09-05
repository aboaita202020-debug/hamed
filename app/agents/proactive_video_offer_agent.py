"""Agent that detects a fit and proactively offers Hamed's video service."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.proactive_video_offer import ProactiveVideoOfferEngine

class ProactiveVideoOfferAgent(BaseAgent):
    name = "proactive_video_offer_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = ProactiveVideoOfferEngine()

    def run(self, payload: dict) -> AgentResult:
        result = self.engine.evaluate(str(payload.get("message", "")), payload.get("context", {}))
        return AgentResult(success=True, data=result, next_actions=[result["next_action"]])
