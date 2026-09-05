"""Video-to-Commerce planning engine."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class VideoCommercePlan:
    product: str
    assets: list[str]
    sales_surface: str
    funnel: list[str]
    content_actions: list[str]
    monetization: list[str]
    next_actions: list[str]

class VideoCommerceEngine:
    def build(self, request: dict[str, Any]) -> dict[str, Any]:
        product = str(request.get("product") or "").strip()
        evidence = list(request.get("evidence") or [])
        videos = list(request.get("video_assets") or [])
        if not product or not evidence:
            return {"status": "needs_validation", "reason": "product_and_verifiable_evidence_required"}
        surface = "existing_store" if request.get("has_store") else ("ecommerce_store" if int(request.get("catalog_size", 1) or 1) > 1 else "landing_page")
        plan = VideoCommercePlan(product, videos, surface, ["landing_or_store", "offer", "whatsapp_or_permitted_contact", "checkout_or_booking", "follow_up", "analytics"], ["audit_existing_video", "extract_verified_product_facts", "create_hooks_and_variants", "add_clear_cta"], ["setup_fee", "monthly_management", "optional_verified_performance_fee"], ["compile_offer", "create_sales_assets", "launch_only_with_permission", "measure_conversion", "optimize"])
        return {"status": "ready_for_planning", "plan": asdict(plan), "evidence": evidence, "approval_boundary": "publishing_paid_spend_orders_payments_and_binding_commitments_require_authorization", "no_guaranteed_results": True}
