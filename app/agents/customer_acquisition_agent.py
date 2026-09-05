"""Customer Acquisition Agent: discover, qualify and missionize buyer signals."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.customer_acquisition import CustomerAcquisitionEngine, LeadSignal

class CustomerAcquisitionAgent(BaseAgent):
    name = "customer_acquisition_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = CustomerAcquisitionEngine()

    def run(self, payload: dict) -> AgentResult:
        signal = LeadSignal(
            source=payload.get("source", "unknown"),
            text=payload.get("text", ""),
            url=payload.get("url", ""),
            contact=payload.get("contact", ""),
            evidence=payload.get("evidence", ""),
            metadata=payload.get("metadata", {}),
        )
        if not signal.text.strip():
            return AgentResult(success=False, error="missing_demand_signal")
        mission = self.engine.build_mission(signal, payload.get("offer", ""))
        return AgentResult(success=True, data=mission, next_actions=["research_lead", "personalized_outreach"])
