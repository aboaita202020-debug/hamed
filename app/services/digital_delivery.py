"""Execution planning for websites, stores, and other digital services.

The builder creates deterministic project specifications. Actual external
publishing/account changes remain behind an explicit authorization boundary.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
import re


@dataclass(frozen=True)
class DigitalProject:
    project_type: str
    business_name: str
    pages: tuple[str, ...]
    features: tuple[str, ...]
    content_tasks: tuple[str, ...]
    quality_checks: tuple[str, ...]
    deployment_status: str = "ready_for_authorized_deployment"


class DigitalDeliveryEngine:
    SITE_DEFAULTS = ("home", "about", "services", "contact")
    STORE_DEFAULTS = ("home", "catalog", "product", "cart", "checkout", "contact")
    CHECKS = ("mobile", "performance", "accessibility", "seo", "security", "links", "checkout")

    def build(self, *, business_name: str, project_type: str = "website",
              requested_features: list[str] | None = None) -> dict[str, Any]:
        name = business_name.strip()
        if not name:
            raise ValueError("business_name is required")
        kind = project_type.strip().lower()
        if kind not in {"website", "store", "ecommerce", "landing_page"}:
            raise ValueError("unsupported project_type")
        pages = self.STORE_DEFAULTS if kind in {"store", "ecommerce"} else self.SITE_DEFAULTS
        features = tuple(dict.fromkeys(requested_features or []))
        if kind in {"store", "ecommerce"}:
            features = tuple(dict.fromkeys([*features, "product_catalog", "cart", "checkout", "order_tracking"]))
        content_tasks = ("business_profile", "offers", "contact_details", "legal_pages")
        quality = self.CHECKS if kind in {"store", "ecommerce"} else tuple(x for x in self.CHECKS if x != "checkout")
        project = DigitalProject(kind, name, pages, features, content_tasks, quality)
        return asdict(project)

    def validate_content(self, content: dict[str, Any]) -> dict[str, Any]:
        text = " ".join(str(v) for v in content.values() if v is not None)
        return {"has_content": bool(text.strip()), "has_placeholder_tokens": bool(re.search(r"lorem|example\.com|TODO", text, re.I)),
                "status": "review_required" if not text.strip() or re.search(r"lorem|example\.com|TODO", text, re.I) else "content_present"}

    def deployment_plan(self, project: dict[str, Any]) -> dict[str, Any]:
        return {"project": project, "steps": ["build", "test", "accessibility_check", "seo_check", "security_check", "human_approval", "deploy"],
                "deployment_authorized": False}
