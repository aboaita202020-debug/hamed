"""Agent for discovering multiple legitimate revenue paths from one customer."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.revenue_path_engine import RevenuePathEngine


class RevenuePathAgent(BaseAgent):
    name = "revenue_path_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = RevenuePathEngine()

    def run(self, payload: dict) -> AgentResult:
        try:
            return AgentResult(success=True, data=self.engine.discover(payload))
        except Exception as exc:
            return AgentResult(success=False, error=str(exc))
