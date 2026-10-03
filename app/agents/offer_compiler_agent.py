"""Offer Compiler Agent: turns verified customer needs into personalized offers."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.offer_compiler import OfferCompiler

class OfferCompilerAgent(BaseAgent):
    name = "offer_compiler_agent"

    def __init__(self, tools, repo):
        super().__init__(tools, repo)
        self.compiler = OfferCompiler()

    def run(self, payload: dict) -> AgentResult:
        try:
            offer = self.compiler.compile(
                customer=payload.get("customer", ""),
                problem=payload.get("problem", ""),
                services=list(payload.get("services") or []),
                deliverables=list(payload.get("deliverables") or []),
                price=payload.get("price"),
                expected_result=payload.get("expected_result"),
                terms=list(payload.get("terms") or []),
                confidence=float(payload.get("confidence", 0)),
                evidence=list(payload.get("evidence") or []),
                cta=payload.get("cta", "start with a scoped pilot"),
            )
            presentation = self.compiler.choose_presentation(
                payload.get("customer_state", "unknown"),
                concise=bool(payload.get("concise", False)),
            )
            offer["presentation"] = presentation
            return AgentResult(success=True, data=offer, next_actions=["sales_message", "negotiation_if_authorized"])
        except (TypeError, ValueError) as exc:
            return AgentResult(success=False, error=str(exc))
