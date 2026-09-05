from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.opportunity_machine import OpportunityMachine

class OpportunityMachineAgent(BaseAgent):
    name = "opportunity_machine"
    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.machine = OpportunityMachine()
    def run(self, payload: dict) -> AgentResult:
        signal = payload.get("signal") or payload
        if not isinstance(signal, dict):
            return AgentResult(False, error="signal must be an object")
        return AgentResult(True, data=self.machine.snapshot(signal), next_actions=["execute_queued_missions"])
