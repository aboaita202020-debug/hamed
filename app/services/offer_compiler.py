"""Personalized service-offer compiler for Hamed AI.

Compiles evidence-backed offers without inventing prices, ROI, capabilities, or facts.
It prepares an offer; final financial/binding actions remain subject to permissions.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class OfferBrief:
    customer: str
    problem: str
    value_proposition: str
    services: tuple[str, ...]
    deliverables: tuple[str, ...]
    price: float | None
    expected_result: str | None
    terms: tuple[str, ...]
    call_to_action: str
    confidence: float

class OfferCompiler:
    def compile(self, *, customer: str, problem: str, services: list[str],
                deliverables: list[str] | None = None, price: float | None = None,
                expected_result: str | None = None, terms: list[str] | None = None,
                confidence: float = 0.0, evidence: list[str] | None = None,
                cta: str = "start with a scoped pilot") -> dict[str, Any]:
        if not customer.strip() or not problem.strip():
            raise ValueError("customer and problem are required")
        if not services:
            raise ValueError("at least one service is required")
        if price is not None and price < 0:
            raise ValueError("price cannot be negative")
        if not 0 <= confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        evidence = list(evidence or [])
        return {
            "customer": customer,
            "problem": problem,
            "value_proposition": f"Address {problem} with {', '.join(services)}.",
            "services": list(services),
            "deliverables": list(deliverables or []),
            "price": price,
            "price_status": "provided" if price is not None else "not_set",
            "expected_result": expected_result,
            "terms": list(terms or []),
            "call_to_action": cta,
            "confidence": confidence,
            "evidence": evidence,
            "personalized": True,
            "binding_action_required": True,
            "no_invented_claims": True,
        }

    def choose_presentation(self, customer_state: str, *, concise: bool = False) -> dict[str, Any]:
        state = customer_state.lower().strip()
        if state in {"urgent", "ready_to_buy", "ready"}:
            mode = "result_price_next_step"
        elif state in {"hesitant", "uncertain"}:
            mode = "pilot_trust_risk_reduction"
        elif state in {"researching", "detail_oriented"}:
            mode = "evidence_comparison_roi_risks"
        else:
            mode = "problem_value_proof_next_step"
        return {"mode": mode, "concise": concise}
