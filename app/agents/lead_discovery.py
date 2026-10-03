"""Lead discovery and ethical outreach planning."""
from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class Lead:
    name: str
    business: str
    channel: str
    source: str
    need: str = ""
    contact: str = ""
    verified: bool = False
    opted_out: bool = False


def qualify(leads: list[Lead]) -> list[Lead]:
    return [x for x in leads if x.verified and not x.opted_out]


def outreach_plan(lead: Lead, service: str, problem: str) -> dict:
    return {"lead": asdict(lead), "service": service, "problem": problem, "requires_opt_in_or_permitted_contact": True, "ai_disclosure": True}
