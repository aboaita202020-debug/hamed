"""Legitimate social-media growth planning and execution queue.

The engine focuses on authentic audience growth, content, engagement, leads,
and measurable sales. It never creates fake engagement or bypasses platform
controls. Actual publishing/engagement is delegated to an authorized adapter.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any


PLATFORMS = ("facebook", "instagram", "tiktok", "youtube", "linkedin", "x")
GOALS = ("awareness", "followers", "engagement", "leads", "sales", "local_reach", "brand")


@dataclass(frozen=True)
class SocialGrowthPlan:
    platform: str
    goal: str
    audience: str
    cadence: str
    content_pillars: tuple[str, ...]
    actions: tuple[str, ...]
    kpis: tuple[str, ...]
    requires_connection: bool = True


class SocialGrowthEngine:
    """Build evidence-based growth plans and safe action queues."""

    def audit(self, evidence: dict[str, Any]) -> dict[str, Any]:
        return {
            "platform": evidence.get("platform"),
            "followers": evidence.get("followers"),
            "engagement_rate": evidence.get("engagement_rate"),
            "reach": evidence.get("reach"),
            "top_content": evidence.get("top_content", []),
            "weak_content": evidence.get("weak_content", []),
            "audience": evidence.get("audience"),
            "evidence": evidence.get("evidence", []),
            "hypotheses": evidence.get("hypotheses", []),
        }

    def plan(self, *, platform: str, goal: str = "followers", audience: str = "target customers", cadence: str = "daily") -> SocialGrowthPlan:
        platform = platform.lower().strip()
        goal = goal.lower().strip()
        if platform not in PLATFORMS:
            raise ValueError("unsupported social platform")
        if goal not in GOALS:
            raise ValueError("unsupported social growth goal")
        return SocialGrowthPlan(
            platform=platform,
            goal=goal,
            audience=audience,
            cadence=cadence,
            content_pillars=("customer-problems", "useful-education", "proof-and-results", "offers", "community"),
            actions=(
                "create_content_calendar",
                "publish_original_content",
                "optimize_hooks_and_ctas",
                "engage_with_relevant_conversations",
                "review_analytics",
                "iterate_on_winning_content",
                "convert_interest_to_leads",
            ),
            kpis=("followers", "reach", "engagement_rate", "profile_visits", "leads", "sales"),
        )

    def action_queue(self, plan: SocialGrowthPlan, *, connected: bool = False) -> list[dict[str, Any]]:
        return [
            {
                "action": action,
                "platform": plan.platform,
                "status": "ready" if connected else "waiting_for_authorized_connection",
                "requires_authorized_connection": action in {"publish_original_content", "engage_with_relevant_conversations"},
                "requires_approval": action == "publish_original_content",
            }
            for action in plan.actions
        ]

    def recommend_services(self, *, goal: str = "followers") -> list[str]:
        goal = goal.lower().strip()
        if goal not in GOALS:
            raise ValueError("unsupported social growth goal")
        mapping = {
            "awareness": ["social-media-management", "content-production"],
            "followers": ["social-media-management", "content-production", "social-growth"],
            "engagement": ["social-media-management", "content-production"],
            "leads": ["social-media-management", "social-lead-generation", "conversion-optimization"],
            "sales": ["social-media-management", "social-lead-generation", "conversion-optimization", "ads-management"],
            "local_reach": ["social-media-management", "content-production", "social-lead-generation"],
            "brand": ["social-media-management", "content-production"],
        }
        return mapping[goal]
