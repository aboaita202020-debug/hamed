"""UGC Video Factory for ORVIA digital marketing.

Planning/orchestration layer for UGC creatives. It does not claim that a video
was rendered or published unless an external production/publishing tool verifies it.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any

@dataclass
class UGCConcept:
    concept_id: str
    product: str
    audience: str
    platform: str
    format: str
    hook: str
    script: str
    cta: str
    status: str = "planned"
    execution_proof: dict[str, Any] | None = None

class UGCVideoFactory:
    FORMATS = (
        "product_review", "unboxing", "testimonial_style", "problem_solution",
        "before_after", "product_demo", "how_to", "storytelling",
        "comparison", "faq", "reaction", "lifestyle", "short_form_ad",
    )
    PLATFORMS = ("tiktok", "instagram_reels", "youtube_shorts", "facebook", "snapchat", "landing_page")

    def __init__(self) -> None:
        self.concepts: list[UGCConcept] = []

    def create_concept(self, product: str, audience: str, platform: str,
                       format: str = "problem_solution", hook: str = "",
                       script: str = "", cta: str = "") -> UGCConcept:
        if not product.strip():
            raise ValueError("product is required")
        if platform not in self.PLATFORMS:
            raise ValueError(f"unsupported platform: {platform}")
        if format not in self.FORMATS:
            raise ValueError(f"unsupported format: {format}")
        now = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        item = UGCConcept(
            concept_id=f"ugc_{now}", product=product.strip(), audience=audience.strip(),
            platform=platform, format=format, hook=hook.strip(),
            script=script.strip(), cta=cta.strip()
        )
        self.concepts.append(item)
        return item

    def status(self) -> dict[str, Any]:
        return {
            "status": "ready",
            "concepts": len(self.concepts),
            "formats": list(self.FORMATS),
            "platforms": list(self.PLATFORMS),
            "production_verified": False,
            "publication_verified": False,
            "reality_rule": "planned is not executed; executed requires tool proof; published requires platform verification",
        }

    def brief(self, product: str, audience: str, platform: str) -> dict[str, Any]:
        return {
            "status": "ready",
            "workflow": [
                "market_research", "audience_research", "customer_psychology",
                "ugc_concept", "hook", "script", "voice_or_avatar",
                "visual_production", "editing", "quality_check",
                "platform_version", "publish_when_authorized", "analytics", "learning"
            ],
            "product": product,
            "audience": audience,
            "platform": platform,
        }

ugc_video_factory = UGCVideoFactory()
