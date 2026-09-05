"""Proactively surface Hamed's video-creation service when a customer is a fit."""
from __future__ import annotations
from typing import Any

VIDEO_SIGNALS = (
    "فيديو", "فيديوهات", "video", "videos", "ريلز", "reels", "تيك توك",
    "tiktok", "اعلان", "إعلان", "ads", "content", "محتوى", "تصوير",
    "مونتاج", "edit", "creative", "منتج", "منتجات", "product", "products",
)

class ProactiveVideoOfferEngine:
    def evaluate(self, message: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        text = (message or "").strip().lower()
        context = context or {}
        if not text:
            return {"eligible": False, "reason": "empty_message"}
        if context.get("opt_out"):
            return {"eligible": False, "reason": "opted_out"}
        matched = [signal for signal in VIDEO_SIGNALS if signal in text]
        eligible = bool(matched)
        return {
            "eligible": eligible,
            "signal_count": len(matched),
            "matched_signals": matched,
            "service": "video_creation",
            "offer": (
                "أقدر أعملك فيديو كامل لمنتجك أو خدمتك: فكرة + Hook + Script + "
                "Storyboard + إنتاج/مونتاج + CTA ونسخ مناسبة للمنصات. "
                "ابعتلي المنتج والمعلومات المتاحة ونبدأ."
            ) if eligible else None,
            "next_action": "route_to_video_production_agent" if eligible else "continue_discovery",
            "truth_boundary": "لا يتم اختلاق مواصفات أو نتائج أو شهادات للمنتج.",
            "approval_boundary": "النشر والإعلانات المدفوعة وأي التزام مالي أو تعاقدي يحتاج صلاحية مناسبة.",
        }
