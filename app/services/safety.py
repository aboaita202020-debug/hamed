"""Policy boundaries for outreach, review, autonomy and high-impact actions."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class OutreachPolicy:
    rate_limit_per_hour: int = 20
    require_public_evidence: bool = True
    allow_mass_messaging: bool = False
    allow_private_scraping: bool = False
    opt_out_required: bool = True

    def validate(self, *, evidence: list[str], opted_out: bool = False) -> bool:
        if opted_out or (self.require_public_evidence and not evidence): return False
        return True

class Critic:
    """Deterministic pre-send gate. A model reviewer may be layered above this."""
    FORBIDDEN = ("guaranteed", "fake review", "password", "api key", "credit card")
    def review(self, text: str, evidence: list[str] | None = None) -> dict:
        evidence=evidence or []
        reasons=[]
        if not evidence: reasons.append("missing evidence")
        low=text.lower()
        if any(x in low for x in self.FORBIDDEN): reasons.append("unsafe or unsupported content")
        return {"approved": not reasons, "reasons": reasons, "evidence_verified": bool(evidence)}

class AutonomyPolicy:
    HIGH_IMPACT={"purchase","payment","transfer","contract","publish","account_change","irreversible"}
    def allowed(self, action: str, *, explicit_approval: bool = False) -> bool:
        return action not in self.HIGH_IMPACT or explicit_approval

__all__=["OutreachPolicy","Critic","AutonomyPolicy"]
