"""Policy-aware supervisor for Hamed's commercial agent network."""
from __future__ import annotations
from dataclasses import dataclass
from .permissions import Risk, can_execute

@dataclass(frozen=True)
class SupervisionDecision:
    action: str
    allowed: bool
    approval_required: bool
    risk: str
    reason: str

class HamedSupervisor:
    """Central gate before any consequential tool call."""
    def inspect(self, action: str, *, value: float | None = None, risk: Risk = Risk.LOW,
                approved: bool = False) -> SupervisionDecision:
        allowed = can_execute(action, approved=approved, value=value, risk=risk)
        approval_required = not allowed and not approved
        reason = "approved" if approved and allowed else ("allowed_by_policy" if allowed else "explicit_approval_required")
        return SupervisionDecision(action, allowed, approval_required, risk.value, reason)

    def require(self, action: str, *, value: float | None = None, risk: Risk = Risk.LOW,
                approved: bool = False) -> None:
        decision = self.inspect(action, value=value, risk=risk, approved=approved)
        if not decision.allowed:
            raise PermissionError(f"Hamed blocked action '{action}': {decision.reason}")
