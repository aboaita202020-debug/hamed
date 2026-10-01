"""Sales policy primitives + SalesAgent pipeline."""
from __future__ import annotations
from dataclasses import dataclass
from app.db.models import PIPELINE_STAGES, Proposal
from .base_agent import BaseAgent, AgentResult

@dataclass(frozen=True)
class SalesLimits:
    minimum_price: float
    maximum_discount_percent: float = 0.0
    def validate_price(self, price: float, list_price: float) -> bool:
        if price < self.minimum_price:
            return False
        if list_price > 0:
            discount = (list_price - price) / list_price * 100
            return discount <= self.maximum_discount_percent
        return True

def negotiate_within_limits(proposed_price: float, list_price: float, limits: SalesLimits) -> str:
    if limits.validate_price(proposed_price, list_price):
        return "approved_within_limits"
    return "escalate_for_approval"

class SalesAgent(BaseAgent):
    name = "sales_agent"
    def run(self, payload: dict) -> AgentResult:
        lead_id = payload.get("lead_id")
        action = payload.get("action")
        lead = self.repo.get_lead(lead_id) if lead_id else None
        if not lead:
            return AgentResult(success=False, error="lead_not_found")
        if action == "advance_stage":
            stage = payload.get("stage")
            if stage not in PIPELINE_STAGES:
                return AgentResult(success=False, error=f"invalid_stage:{stage}")
            self.repo.update_lead_stage(lead_id, stage)
            return AgentResult(success=True, data={"lead_id": lead_id, "stage": stage})
        if action == "create_proposal":
            proposal = self.repo.add_proposal(Proposal(lead_id=lead_id, service=payload.get("service", ""), price=payload.get("price", 0.0), status="SENT"))
            self.repo.update_lead_stage(lead_id, "PROPOSAL")
            deal = self.repo.open_deal(lead_id, proposal.id, expected_revenue=proposal.price)
            return AgentResult(success=True, data={"proposal": proposal, "deal": deal}, next_actions=["negotiation_or_close"])
        return AgentResult(success=False, error=f"unknown_action:{action}")
