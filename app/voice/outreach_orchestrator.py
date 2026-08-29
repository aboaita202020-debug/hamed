"""Arabic-market outreach orchestration for Hamed.

Free-first, policy-aware routing layer. It decides *how* Hamed should approach
an eligible prospect; it does not bypass consent, DNC, telecom rules, or
provider restrictions.
"""
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional

from app.voice.arab_world_policy import ArabWorldPolicy


@dataclass
class Prospect:
    name: str
    country: str
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    consented: bool = False
    do_not_contact: bool = False
    business: Optional[str] = None
    website: Optional[str] = None


@dataclass
class OutreachPlan:
    eligible: bool
    country: str
    timezone: str
    currency: str
    language: str
    channel: str
    objective: str
    reason: str


class OutreachOrchestrator:
    """Builds a compliant, localized outreach plan for Arabic prospects."""

    def __init__(self, policy: Optional[ArabWorldPolicy] = None):
        self.policy = policy or ArabWorldPolicy()

    def plan(self, prospect: Prospect, now: Optional[datetime] = None) -> OutreachPlan:
        country = prospect.country.strip().lower()
        profile = self.policy.profile_for(country)
        if profile is None:
            return OutreachPlan(False, country, "", "", "ar", "none", "none", "Country is outside the configured Arabic-market scope")

        if prospect.do_not_contact:
            return OutreachPlan(False, country, profile.timezone, profile.currency, profile.language, "none", "none", "Prospect opted out")

        # Outbound marketing calls require the configured legal/telecom path.
        # For unsolicited prospects, prefer a non-call channel unless consent exists.
        if prospect.consented and prospect.phone:
            channel = "voice"
            reason = "Consent/eligibility allows voice outreach; provider and local telecom checks still required"
        elif prospect.whatsapp:
            channel = "whatsapp"
            reason = "Use a non-call channel until voice eligibility is established"
        elif prospect.email:
            channel = "email"
            reason = "Use email until a permitted conversational channel is available"
        else:
            channel = "none"
            reason = "No permitted contact channel is available"

        objective = "discovery_and_value_assessment"
        return OutreachPlan(True, country, profile.timezone, profile.currency, profile.language, channel, objective, reason)

    def is_local_business_hours(self, plan: OutreachPlan, now: Optional[datetime] = None) -> bool:
        if not plan.eligible or not plan.timezone:
            return False
        current = now or datetime.now(ZoneInfo("UTC"))
        local = current.astimezone(ZoneInfo(plan.timezone))
        # Conservative default; country-specific rules can be added to policy.
        return 09 <= local.hour < 18 and local.weekday() < 5
