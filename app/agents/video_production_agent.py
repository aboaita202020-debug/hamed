"""Client Video Production Agent."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.video_production import VideoProductionEngine

class VideoProductionAgent(BaseAgent):
    name = "video_production_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = VideoProductionEngine()

    def run(self, payload: dict) -> AgentResult:
        result = self.engine.build(payload)
        if result["status"] == "needs_input":
            actions = ["collect_video_brief"]
        elif result["status"] == "needs_validation":
            actions = ["collect_verified_product_evidence", "verify_brand_assets_and_claims"]
        else:
            actions = result["plan"]["next_actions"]
        return AgentResult(success=result["status"] == "ready_for_planning", data=result, next_actions=actions)
