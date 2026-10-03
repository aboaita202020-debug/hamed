"""Video-to-Commerce Agent."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.video_commerce import VideoCommerceEngine

class VideoCommerceAgent(BaseAgent):
    name = "video_commerce_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = VideoCommerceEngine()

    def run(self, payload: dict) -> AgentResult:
        result = self.engine.build(payload)
        actions = result.get("plan", {}).get("next_actions", ["collect_product_evidence"])
        return AgentResult(success=result["status"] == "ready_for_planning", data=result, next_actions=actions)
