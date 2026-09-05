"""Revenue Compiler Agent: select and explain monetization models."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.revenue_compiler import RevenueCompiler

class RevenueCompilerAgent(BaseAgent):
    name = "revenue_compiler_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = RevenueCompiler()

    def run(self, payload: dict) -> AgentResult:
        result = self.engine.compile(payload)
        return AgentResult(success=result["status"] == "compiled", data=result, next_actions=["validate_revenue_model"] if result["status"] == "compiled" else ["collect_evidence"])
