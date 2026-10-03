"""Agent wrapper for universal customer understanding and execution planning."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.universal_customer_execution import UniversalCustomerExecutionEngine

class UniversalCustomerExecutionAgent(BaseAgent):
    name = "universal_customer_execution_agent"

    def run(self, payload: dict) -> AgentResult:
        result = UniversalCustomerExecutionEngine().execute_plan(
            str((payload or {}).get("message") or (payload or {}).get("request") or ""),
            (payload or {}).get("customer") or {},
        )
        intent = result["intent"]
        if intent["status"] == "needs_input":
            actions = ["ask_minimum_clarifying_question"]
        elif intent["status"] == "needs_clarification":
            actions = ["ask_missing_critical_information", "verify_critical_facts"]
        else:
            actions = ["select_specialist", "prepare_execution", "execute", "verify_result", "record_outcome"]
        return AgentResult(True, result, next_actions=actions)
