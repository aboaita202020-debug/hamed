"""Agent that compiles validated requests into new service blueprints."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.service_compiler import ServiceCompiler

class ServiceCompilerAgent(BaseAgent):
    name = "service_compiler_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = ServiceCompiler()

    def run(self, payload: dict) -> AgentResult:
        result = self.engine.compile(payload)
        actions = result.get("blueprint", {}).get("next_actions", ["collect_service_evidence"])
        return AgentResult(success=result["status"] == "compiled", data=result, next_actions=actions)
