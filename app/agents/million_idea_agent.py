"""Agent wrapper for HAMED Million Idea Engine."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.million_idea_engine import MillionIdeaEngine


class MillionIdeaAgent(BaseAgent):
    name = "million_idea_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = MillionIdeaEngine()

    def run(self, payload: dict) -> AgentResult:
        try:
            limit = int(payload.get("limit", 25))
            result = self.engine.generate(payload, limit=limit)
            return AgentResult(success=True, data=result)
        except Exception as exc:
            return AgentResult(success=False, error=str(exc))
