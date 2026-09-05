"""Adaptive marketing campaign planning and monetization."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class CampaignPlan:
    objective: str
    audience: str
    concept: str
    hooks: list[str]
    channels: list[str]
    content_assets: list[str]
    funnel: list[str]
    offer: str
    kpis: list[str]
    monetization: str

class MarketingCampaignEngine:
    def build(self, request: dict[str, Any]) -> dict[str, Any]:
        objective = str(request.get("objective") or "generate qualified customers")
        audience = str(request.get("audience") or "to be researched and validated")
        product = str(request.get("product") or "the customer's offer")
        evidence = list(request.get("evidence") or [])
        if not evidence:
            return {"status": "needs_validation", "reason": "campaign_should_not_assume_market_facts"}
        plan = CampaignPlan(
            objective=objective,
            audience=audience,
            concept=f"Outcome-led campaign for {product}",
            hooks=["problem-first hook", "proof/value hook", "offer/CTA hook"],
            channels=["short_video", "social_content", "search_or_paid_media", "direct_response_channel"],
            content_assets=["campaign_brief", "content_calendar", "short_video_scripts", "ad_copy_variants", "landing_or_chat_offer"],
            funnel=["attention", "qualification", "offer", "conversion", "follow_up", "retention"],
            offer="validated offer with clear deliverables, price and next step",
            kpis=["qualified_leads", "conversion_rate", "customer_acquisition_cost", "revenue", "gross_margin", "return_on_ad_spend_when_applicable"],
            monetization="strategy_fee + campaign_execution + optional monthly management or verified performance fee",
        )
        return {"status": "ready", "plan": asdict(plan), "evidence": evidence, "approval_boundary": "publishing_and_paid_spend_require_authorized_permissions"}
