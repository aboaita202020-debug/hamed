"""Human-centered customer relationship engine for Hamed AI.

The engine helps Hamed build long-term customer relationships without pretending
that the AI is a human. It stores only relationship signals that the application
is explicitly given and uses consent-aware, value-first follow-up rules.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class RelationshipProfile:
    customer_id: str
    name: str = ""
    preferred_channel: str = ""
    preferred_language: str = "ar"
    interests: list[str] = field(default_factory=list)
    important_notes: list[str] = field(default_factory=list)
    last_contact_at: str | None = None
    next_follow_up_at: str | None = None
    consent_status: str = "unknown"
    opt_out: bool = False


class CustomerRelationshipEngine:
    """Turn customer interactions into respectful, useful relationship care."""

    def build_profile(self, payload: dict[str, Any]) -> RelationshipProfile:
        customer_id = str(payload.get("customer_id", "")).strip()
        if not customer_id:
            raise ValueError("customer_id_required")
        return RelationshipProfile(
            customer_id=customer_id,
            name=str(payload.get("name", "")),
            preferred_channel=str(payload.get("preferred_channel", "")),
            preferred_language=str(payload.get("preferred_language", "ar")),
            interests=list(payload.get("interests", []) or []),
            important_notes=list(payload.get("important_notes", []) or []),
            last_contact_at=payload.get("last_contact_at"),
            next_follow_up_at=payload.get("next_follow_up_at"),
            consent_status=str(payload.get("consent_status", "unknown")),
            opt_out=bool(payload.get("opt_out", False)),
        )

    def plan_follow_up(self, profile: RelationshipProfile, reason: str = "value") -> dict[str, Any]:
        if profile.opt_out or profile.consent_status == "revoked":
            return {"action": "do_not_contact", "reason": "customer_opted_out"}
        now = datetime.now(timezone.utc).isoformat()
        return {
            "action": "follow_up",
            "customer_id": profile.customer_id,
            "channel": profile.preferred_channel or "existing_consent_channel",
            "reason": reason,
            "timing": "respect_customer_preference_and_existing_cadence",
            "relationship_goal": "provide_value_and_build_trust",
            "must_not": [
                "pretend_to_be_human",
                "invent_personal_details",
                "pressure_customer",
                "spam_or_bypass_opt_out",
            ],
            "planned_at": now,
        }

    def interaction_summary(self, profile: RelationshipProfile, outcome: str = "") -> dict[str, Any]:
        return {
            "customer_id": profile.customer_id,
            "name": profile.name,
            "interests": profile.interests,
            "important_notes": profile.important_notes,
            "last_contact_at": profile.last_contact_at,
            "outcome": outcome,
            "relationship_principles": [
                "listen",
                "remember_customer_preferences_that_are_provided",
                "follow_up_with_relevant_value",
                "keep_promises",
                "respect_boundaries",
                "make_opt_out_easy",
            ],
        }

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        profile = self.build_profile(payload)
        action = str(payload.get("action", "plan_follow_up"))
        if action == "profile":
            return {"success": True, "profile": profile.__dict__}
        if action == "summary":
            return {"success": True, "summary": self.interaction_summary(profile, str(payload.get("outcome", "")))}
        return {"success": True, "follow_up": self.plan_follow_up(profile, str(payload.get("reason", "value")))}
