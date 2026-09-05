"""Universal customer intake, intent understanding and execution planning."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class CustomerIntent:
    status: str
    customer: dict[str, Any]
    request: str
    intent: str
    needs: list[str]
    missing_information: list[str]
    execution_path: list[str]
    approval_required: bool
    truth_required: bool = True

class UniversalCustomerExecutionEngine:
    INTENTS = {
        "buy": ["buy", "purchase", "عايز اشتري", "عاوز اشتري", "شراء", "مورد"],
        "sell": ["sell", "selling", "عايز ابيع", "عاوز ابيع", "بيع", "عملاء"],
        "build": ["build", "create", "website", "app", "اعمل", "انشاء", "موقع", "متجر"],
        "marketing": ["marketing", "campaign", "تسويق", "حملة", "اعلان", "إعلان"],
        "problem": ["problem", "issue", "مشكل", "مشكلة", "حل"],
        "service": ["service", "خدمة", "خدمه", "محتاج"],
    }

    def understand(self, message: str, customer: dict[str, Any] | None = None) -> CustomerIntent:
        text = (message or "").strip()
        profile = dict(customer or {})
        if not text:
            return CustomerIntent("needs_input", profile, "", "unknown", [], ["request"], ["ask_minimum_clarifying_question"], False)
        low = text.lower()
        scores = {intent: sum(1 for term in terms if term.lower() in low) for intent, terms in self.INTENTS.items()}
        intent = max(scores, key=scores.get)
        if scores[intent] == 0:
            intent = "discovery"
        needs = [text]
        missing = []
        if intent in {"buy", "sell"}: missing += ["product_or_service", "quantity_or_scope"]
        if intent in {"build", "marketing", "service"}: missing += ["goal", "scope"]
        if intent == "problem": missing += ["desired_outcome"]
        known = {k for k, v in profile.items() if v not in (None, "", [])}
        missing = [x for x in missing if x not in known]
        path = ["understand_request", "verify_critical_facts", "select_specialist", "prepare_execution", "execute", "verify_result", "record_outcome"]
        return CustomerIntent("understood" if not missing else "needs_clarification", profile, text, intent, needs, missing[:3], path, intent in {"buy", "sell"})

    def execute_plan(self, message: str, customer: dict[str, Any] | None = None) -> dict[str, Any]:
        intent = self.understand(message, customer)
        return {"customer_status": "customer_opportunity", "intent": asdict(intent), "next_action": intent.execution_path[1] if intent.missing_information else intent.execution_path[2], "autonomous_execution": True, "approval_boundary": "financial_commitments_payments_contracts_regulated_actions_and_irreversible_high_impact_actions_require_authorization", "never_invent_facts": True, "respect_opt_out": True}
