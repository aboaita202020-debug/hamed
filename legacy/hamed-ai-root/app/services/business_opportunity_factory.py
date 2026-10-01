"""Business Opportunity Factory: compose, compare and safely launch revenue experiments."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class FactoryMode:
    key: str
    name: str
    monetization: list[str]

MODES = [
    FactoryMode("opportunity_composer", "Opportunity Composer", ["project_fee", "success_fee"]),
    FactoryMode("business_in_a_box", "Business-in-a-Box Factory", ["setup_fee", "subscription"]),
    FactoryMode("opportunity_genome", "Opportunity Genome", ["subscription", "advisory_fee"]),
    FactoryMode("business_model_mutator", "Business Model Mutator", ["advisory_fee", "subscription"]),
    FactoryMode("spin_off_engine", "Automatic Spin-off Engine", ["setup_fee", "licensing"]),
    FactoryMode("revenue_competition", "Revenue Competition Engine", ["usage_based", "subscription"]),
    FactoryMode("opportunity_auction", "Opportunity Auction", ["transaction_fee", "subscription"]),
    FactoryMode("zero_to_revenue", "Zero-to-Revenue Mission", ["project_fee", "success_fee"]),
]

class BusinessOpportunityFactory:
    def catalog(self) -> list[dict[str, Any]]:
        return [asdict(m) for m in MODES]

    def compose(self, payload: dict[str, Any]) -> dict[str, Any]:
        signal = str(payload.get("signal") or payload.get("problem") or "").strip()
        evidence = list(payload.get("evidence") or [])
        if not signal:
            return {"status": "needs_input", "reason": "missing_opportunity_signal"}
        if not evidence:
            return {"status": "needs_validation", "reason": "evidence_required", "catalog": self.catalog()}
        nodes = payload.get("nodes") or ["problem", "payer", "solution", "channel", "partner", "revenue_model"]
        candidates = self._candidates(payload)
        return {
            "status": "composed",
            "signal": signal,
            "evidence_count": len(evidence),
            "opportunity_graph": nodes,
            "candidates": candidates,
            "competition_rule": "compare candidates using verified unit economics, confidence, execution cost, time-to-first-customer and risk",
            "mission_loop": ["verify", "score", "build_small_test", "find_first_customer", "measure", "learn", "scale_or_kill"],
            "approval_boundary": "payments_contracts_binding_commitments_regulated_actions_and_irreversible_high_impact_actions_require_authorization",
            "no_guaranteed_revenue": True,
        }

    def _candidates(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        modes = self.catalog()
        preferred = str(payload.get("preferred_mode") or "").lower()
        if preferred:
            modes = sorted(modes, key=lambda m: 0 if preferred in m["key"] else 1)
        return [{**m, "test": "smallest_valid_experiment", "requires_verified_outcome": True} for m in modes]
