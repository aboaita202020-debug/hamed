"""ReportingAgent — spec section 20. Builds the Dashboard snapshot."""
from __future__ import annotations

from .base_agent import BaseAgent, AgentResult


class ReportingAgent(BaseAgent):
    name = "reporting_agent"

    def run(self, payload: dict) -> AgentResult:
        snapshot = self.repo.dashboard_snapshot()
        return AgentResult(success=True, data=snapshot)
