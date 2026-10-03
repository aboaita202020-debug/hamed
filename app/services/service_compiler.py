"""Build-on-demand Service Compiler for requests outside the existing catalog."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class ServiceBlueprint:
    request: str
    outcome: str
    capabilities: list[str]
    delivery_steps: list[str]
    revenue_models: list[str]
    next_actions: list[str]

class ServiceCompiler:
    """Turns a validated customer request into a reusable service blueprint."""
    def compile(self, request: dict[str, Any]) -> dict[str, Any]:
        need = str(request.get("request") or request.get("need") or "").strip()
        evidence = list(request.get("evidence") or [])
        if not need:
            return {"status": "needs_input", "reason": "missing_service_request"}
        if not evidence:
            return {"status": "needs_validation", "reason": "verifiable_customer_need_required"}
        outcome = str(request.get("desired_outcome") or "verified customer outcome").strip()
        capabilities = list(request.get("available_capabilities") or ["research", "planning", "specialist_agent", "quality_check"])
        blueprint = ServiceBlueprint(need, outcome, capabilities, ["scope", "assemble_capabilities", "prototype", "quality_check", "price", "offer", "deliver", "verify_outcome", "capture_reusable_knowledge"], ["project_fee", "milestone", "subscription", "usage_based", "verified_performance_fee"], ["compile_offer", "estimate_cost_and_margin", "request_authorization_for_binding_commitments", "deliver_and_measure"])
        return {"status": "compiled", "blueprint": asdict(blueprint), "evidence": evidence, "approval_boundary": "contracts_payments_external_binding_commitments_and_high_impact_actions_require_authorization", "no_guaranteed_result": True}
