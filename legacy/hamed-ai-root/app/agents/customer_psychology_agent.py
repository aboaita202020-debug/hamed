"""Agent wrapper for ethical customer psychology analysis."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.customer_psychology import CustomerPsychologyEngine


class CustomerPsychologyAgent(BaseAgent):
    name = "customer_psychology_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = CustomerPsychologyEngine()

    def run(self, payload: dict) -> AgentResult:
        message = payload.get("message", "")
        profile = self.engine.analyze(message)
        return AgentResult(
            success=True,
            data={
                "profile": profile.__dict__,
                "guidance": self.engine.communication_guidance(profile),
            },
            next_actions=[profile.recommended_next_step],
        )
