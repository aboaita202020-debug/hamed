"""Client video-production planning and monetization engine."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class VideoProductionPlan:
    brief: str
    goal: str
    formats: list[str]
    creative_assets: list[str]
    production_steps: list[str]
    variants: list[str]
    distribution: list[str]
    monetization: list[str]
    next_actions: list[str]

class VideoProductionEngine:
    """Turns a video request into a verifiable production workflow and offer."""

    def build(self, request: dict[str, Any]) -> dict[str, Any]:
        brief = str(request.get("brief") or request.get("request") or "").strip()
        evidence = list(request.get("evidence") or [])
        if not brief:
            return {"status": "needs_input", "reason": "video_request_required"}
        if not evidence:
            return {"status": "needs_validation", "reason": "verified_product_or_client_requirements_required"}

        goal = str(request.get("goal") or "sales_or_brand_awareness").strip()
        formats = list(request.get("formats") or ["reel", "short", "vertical_ad"])
        if request.get("landscape"):
            formats.append("landscape_video")
        duration = str(request.get("duration") or "short_form")
        variants = ["hook_variant_a", "hook_variant_b", "cta_variant"]
        if request.get("languages"):
            variants.extend([f"localized_{str(x)}" for x in request["languages"]])

        plan = VideoProductionPlan(
            brief=brief,
            goal=goal,
            formats=formats,
            creative_assets=[
                "verified_product_facts",
                "script_or_voiceover",
                "storyboard",
                "visual_asset_list",
                "on_screen_text",
                "caption_and_cta",
            ],
            production_steps=[
                "clarify_critical_brief_fields",
                "verify_claims_and_brand_assets",
                "write_script",
                "build_storyboard",
                "produce_or_edit_video",
                "quality_check",
                "create_variants",
                "prepare_distribution_assets",
                "measure_and_optimize",
            ],
            variants=variants,
            distribution=["client_delivery", "permitted_social_channels", "landing_page_or_store", "permitted_messaging_channel"],
            monetization=["one_time_production_fee", "package_fee", "monthly_content_retainer", "optional_performance_fee_when_measurable"],
            next_actions=["compile_video_offer", "prepare_script", "produce_or_edit", "quality_check", "deliver", "measure_and_optimize"],
        )
        return {
            "status": "ready_for_planning",
            "plan": asdict(plan),
            "duration": duration,
            "evidence": evidence,
            "approval_boundary": "publishing_paid_spend_binding_contracts_and_external_commitments_require_authorization",
            "truth_boundary": "never invent product claims testimonials results or performance",
            "no_guaranteed_results": True,
        }
