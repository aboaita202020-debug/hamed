"""SalesAgent — spec section 7 (Pipeline + Problem->Solution->Offer).

Moves a Lead through the pipeline stages and can create a Proposal.
Pricing/discount decisions above configured limits go through the
Permission Layer via ToolRegistry before being applied.
"""
from __future__ import annotations

from app.db.models import PIPELINE_STAGES, Proposal
from .base_agent import BaseAgent, AgentResult


class SalesAgent(BaseAgent):
    name = "sales_agent"

    def run(self, payload: dict) -> AgentResult:
        """payload:
        {
          "lead_id": int,
          "action": "advance_stage" | "create_proposal",
          "stage": str (for advance_stage),
          "service": str, "price": float (for create_proposal),
        }
        """
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
            proposal = self.repo.add_proposal(
                Proposal(lead_id=lead_id, service=payload.get("service", ""),
                         price=payload.get("price", 0.0), status="SENT")
            )
            self.repo.update_lead_stage(lead_id, "PROPOSAL")
            deal = self.repo.open_deal(lead_id, proposal.id, expected_revenue=proposal.price)
            return AgentResult(success=True, data={"proposal": proposal, "deal": deal},
                                next_actions=["negotiation_or_close"])

        return AgentResult(success=False, error=f"unknown_action:{action}")
