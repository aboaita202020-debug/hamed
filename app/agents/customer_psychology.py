"""Customer understanding without protected-trait profiling or coercion."""
from __future__ import annotations

def customer_profile(needs: list[str], pain_points: list[str], objections: list[str], decision_factors: list[str]) -> dict:
    return {"needs": needs, "pain_points": pain_points, "objections": objections, "decision_factors": decision_factors, "protected_trait_inference": False, "coercive_manipulation": False}


def response_framework(problem: str, value: str, objection: str = "") -> list[str]:
    result = [f"acknowledge:{problem}", f"explain_value:{value}"]
    if objection:
        result.append(f"address_objection:{objection}")
    result.append("offer_clear_next_step")
    return result
