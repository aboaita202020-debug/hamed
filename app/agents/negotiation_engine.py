"""Bounded negotiation strategy builder."""
from __future__ import annotations

def strategy(target: float, minimum: float, max_discount_percent: float = 20.0, concessions: list[str] | None = None) -> dict:
    if minimum < 0 or target < minimum or not 0 <= max_discount_percent <= 100:
        raise ValueError("Invalid negotiation boundaries")
    return {"target": target, "minimum": minimum, "max_discount_percent": max_discount_percent, "concessions": concessions or [], "walk_away": minimum, "no_fake_claims": True}
