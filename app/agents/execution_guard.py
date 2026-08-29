"""Final server-side execution gate for commercial actions."""
from dataclasses import dataclass

from .autonomy import policy
from .permissions import can_execute


@dataclass(frozen=True)
class ExecutionDecision:
    action: str
    allowed: bool
    reason: str


def authorize(action: str, approved: bool = False, value: float | None = None) -> ExecutionDecision:
    # Explicit approval always satisfies the existing permission gate.
    if approved and can_execute(action, approved=True):
        return ExecutionDecision(action, True, "explicitly_approved")

    # Autonomous execution is bounded by server-side policy and never applies to
    # contracts, publishing, account changes, or irreversible operations.
    if policy.allows(action, value=value):
        return ExecutionDecision(action, True, "authorized_by_autonomy_policy")

    if action in {"purchase", "payment", "transfer", "contract", "publish", "account_change", "irreversible"}:
        return ExecutionDecision(action, False, "outside_autonomy_policy_or_approval_required")

    return ExecutionDecision(action, True, "authorized")
