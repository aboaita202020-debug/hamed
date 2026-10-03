"""RevenueAgent — spec section 5.

Aggregates pipeline + revenue-event data into the metrics the spec
requires: Expected vs Actual revenue, Conversion, Close Rate.
"""
from __future__ import annotations

from .base_agent import BaseAgent, AgentResult


class RevenueAgent(BaseAgent):
    name = "revenue_agent"

    def run(self, payload: dict) -> AgentResult:
        metrics = self.repo.pipeline_metrics()
        return AgentResult(success=True, data=metrics)
