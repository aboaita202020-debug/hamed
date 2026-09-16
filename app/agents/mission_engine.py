"""Unified mission engine for Hamed AGI.

Converts a business objective into a deterministic, auditable execution plan.
The engine coordinates research, opportunity discovery, economics, leads,
sales, website/service work, experiments, learning and reporting while keeping
sensitive actions behind the existing permission layer.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class MissionStep:
    id: str
    capability: str
    action: str
    status: str = "planned"
    approval_required: bool = False


CAPABILITY_ROUTES = {
    "commerce": [
        ("research", "market_research"),
        ("opportunity", "opportunity_hunt"),
        ("economics", "unit_economics"),
        ("supplier", "supplier_research"),
        ("negotiation", "negotiate"),
        ("sales", "sale"),
        ("learning", "learn_from_result"),
        ("reporting", "report"),
    ],
    "affiliate": [
        ("research", "affiliate_research"),
        ("opportunity", "opportunity_hunt"),
        ("content", "content_plan"),
        ("marketing", "affiliate_marketing"),
        ("experiment", "run_experiment"),
        ("learning", "learn_from_result"),
        ("reporting", "report"),
    ],
    "service": [
        ("research", "market_research"),
        ("lead_discovery", "lead_generation"),
        ("psychology", "customer_psychology"),
        ("offer", "offer_build"),
        ("sales", "sale"),
        ("delivery", "service_delivery"),
        ("experiment", "run_experiment"),
        ("learning", "learn_from_result"),
        ("reporting", "report"),
    ],
    "website": [
        ("audit", "website_audit"),
        ("lead_discovery", "lead_generation"),
        ("psychology", "customer_psychology"),
        ("offer", "offer_build"),
        ("sales", "sale"),
        ("factory", "website_service"),
        ("quality", "quality_check"),
        ("learning", "learn_from_result"),
        ("reporting", "report"),
    ],
    "marketing": [
        ("research", "market_research"),
        ("psychology", "customer_psychology"),
        ("content", "content_plan"),
        ("marketing", "marketing"),
        ("experiment", "run_experiment"),
        ("learning", "learn_from_result"),
        ("reporting", "report"),
    ],
    "b2b": [
        ("research", "market_research"),
        ("buyers", "lead_generation"),
        ("suppliers", "supplier_research"),
        ("match", "b2b_match"),
        ("negotiation", "negotiate"),
        ("sales", "sale"),
        ("learning", "learn_from_result"),
        ("reporting", "report"),
    ],
    "general": [
        ("research", "market_research"),
        ("opportunity", "opportunity_hunt"),
        ("council", "council_decision"),
        ("execution", "execute_safe_actions"),
        ("learning", "learn_from_result"),
        ("reporting", "report"),
    ],
}

SENSITIVE_ACTIONS = {"purchase", "payment", "contract", "account_change", "irreversible", "publish"}


def infer_domain(goal: str) -> str:
    text = goal.lower()
    groups = {
        "affiliate": ("affiliate", "عمولة", "تسويق بالعمولة"),
        "website": ("website", "store", "موقع", "متجر", "ecommerce", "تجارة إلكترونية"),
        "b2b": ("b2b", "شركة", "مورد", "supplier", "وساطة"),
        "commerce": ("شراء", "بيع", "منتج", "تجارة", "استيراد", "arbitrage"),
        "marketing": ("marketing", "تسويق", "حملة", "إعلان"),
        "service": ("خدمة", "service", "freelance", "فريلانس"),
    }
    for domain, keywords in groups.items():
        if any(k in text for k in keywords):
            return domain
    return "general"


def build_mission(goal: str, domain: str | None = None) -> list[dict[str, Any]]:
    domain = domain or infer_domain(goal)
    route = CAPABILITY_ROUTES.get(domain, CAPABILITY_ROUTES["general"])
    return [
        asdict(MissionStep(
            id=f"step-{i:02d}",
            capability=capability,
            action=action,
            approval_required=action in SENSITIVE_ACTIONS,
        ))
        for i, (capability, action) in enumerate(route, 1)
    ]
