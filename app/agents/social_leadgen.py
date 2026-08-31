"""Social lead discovery orchestration.

This module defines a provider-neutral interface. Production connectors must
use each platform's official API/approved integration and respect its terms,
privacy rules, rate limits, and user consent requirements.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Lead:
    platform: str
    handle: str
    profile_url: str
    reason: str
    score: float = 0.0


class SocialLeadProvider(Protocol):
    platform: str

    def search(self, query: str, limit: int = 20) -> list[Lead]: ...


class SocialLeadEngine:
    """Search enabled social platforms through approved providers."""

    def __init__(self, providers: list[SocialLeadProvider] | None = None) -> None:
        self.providers = providers or []

    def discover(self, query: str, limit_per_platform: int = 20) -> list[Lead]:
        leads: list[Lead] = []
        seen: set[tuple[str, str]] = set()
        for provider in self.providers:
            try:
                for lead in provider.search(query, limit_per_platform):
                    key = (lead.platform.lower(), lead.handle.lower())
                    if key not in seen:
                        seen.add(key)
                        leads.append(lead)
            except Exception:
                # A single platform outage must not stop prospecting elsewhere.
                continue
        return sorted(leads, key=lambda x: x.score, reverse=True)
