"""Agent for long-term, consent-aware customer relationship care."""
from __future__ import annotations

from .base_agent import AgentResult, BaseAgent
from app.services.customer_relationship import CustomerRelationshipEngine


class CustomerRelationshipAgent(BaseAgent):
    name = "customer_relationship_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = CustomerRelationshipEngine()

    def run(self, payload: dict) -> AgentResult:
        try:
            result = self.engine.run(payload)
            return AgentResult(
                success=True,
                data=result,
                next_actions=[
                    "record_customer_interaction_outcome",
                    "offer_relevant_value_when_due",
                    "respect_channel_preferences_and_opt_out",
                ],
            )
        except (ValueError, TypeError) as exc:
            return AgentResult(success=False, error=str(exc))
