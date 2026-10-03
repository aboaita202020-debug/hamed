"""NegotiationAgent — spec section 9.

Computes a bounded counter-offer. Never exceeds
`ApprovalLimits.max_auto_negotiation_concession_pct`; anything beyond
that must go through the Permission Layer (raises via ToolRegistry,
here we just refuse and flag for approval).
"""
from __future__ import annotations

from app.config import settings
from .base_agent import BaseAgent, AgentResult


class NegotiationAgent(BaseAgent):
    name = "negotiation_agent"

    def run(self, payload: dict) -> AgentResult:
        """payload: {"target_price": float, "counter_offer": float, "minimum_price": float}"""
        target = payload.get("target_price", 0.0)
        counter = payload.get("counter_offer", 0.0)
        minimum = payload.get("minimum_price", 0.0)

        if target <= 0 or minimum <= 0:
            return AgentResult(success=False, error="invalid_target_or_minimum")

        max_concession_pct = settings.approval_limits.max_negotiation_concession_pct
        floor_price = target * (1 - max_concession_pct / 100.0)
        floor_price = max(floor_price, minimum)

        if counter >= floor_price:
            return AgentResult(
                success=True,
                data={
                    "decision": "accept" if counter >= target else "counter",
                    "proposed_price": max(counter, floor_price),
                    "floor_price": floor_price,
                },
            )

        return AgentResult(
            success=False,
            error="counter_below_floor_requires_human_approval",
            next_actions=["escalate_to_owner"],
            data={"floor_price": floor_price, "offer_received": counter},
        )
