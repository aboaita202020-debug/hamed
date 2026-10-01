"""One-customer-to-many-revenue-path discovery engine."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class RevenuePath:
    path: str
    reason: str
    revenue_model: str
    recurring: bool
    approval_required: bool


class RevenuePathEngine:
    PATHS = [
        ("core_service", "Directly solve the verified customer need", "project_fee", False, False),
        ("upsell", "Add a higher-value adjacent outcome", "project_fee", False, False),
        ("cross_sell", "Add a complementary verified service/product", "project_fee", False, False),
        ("subscription", "Turn a recurring need into ongoing service", "subscription", True, False),
        ("retainer", "Provide ongoing managed execution", "retainer", True, False),
        ("referral", "Create a consent-based referral path", "referral_fee", False, True),
        ("affiliate", "Recommend relevant third-party offers where permitted", "referral_fee", False, True),
        ("automation", "Automate a repetitive business process", "project_fee", False, False),
        ("data_product", "Package verified, lawful aggregate insights", "subscription", True, False),
        ("partnership", "Match with a complementary provider", "success_fee", False, True),
    ]

    def discover(self, customer: dict[str, Any]) -> dict[str, Any]:
        signal = str(customer.get("need") or customer.get("signal") or "").strip()
        evidence = customer.get("evidence") or []
        if not signal:
            return {"success": True, "status": "needs_input", "next_actions": ["understand_customer_need"]}
        if not evidence:
            return {"success": True, "status": "needs_validation", "next_actions": ["collect_evidence", "verify_customer_need"]}
        paths = [RevenuePath(*p) for p in self.PATHS]
        return {
            "success": True,
            "status": "discovered",
            "customer_signal": signal,
            "revenue_paths": [asdict(p) for p in paths],
            "next_actions": ["score_paths", "select_best_fit", "compile_offer", "run_small_experiment", "measure_outcome"],
            "boundaries": ["no_spam", "no_fake_claims", "respect_opt_out", "payments_and_binding_commitments_require_authorization"],
        }
