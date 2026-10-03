"""Customer Conversation Agent for adaptive discovery and sales dialogue."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.customer_conversation import CustomerConversationEngine

class CustomerConversationAgent(BaseAgent):
    name = "customer_conversation_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.engine = CustomerConversationEngine()

    def run(self, payload: dict) -> AgentResult:
        message = str(payload.get("message", ""))
        result = self.engine.next_turn(message, payload.get("context", {}))
        return AgentResult(success=True, data=result, next_actions=[result["suggested_action"]])
