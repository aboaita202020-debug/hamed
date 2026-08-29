"""Final execution gate for high-impact commercial actions."""
from dataclasses import dataclass
from .permissions import can_execute


@dataclass(frozen=True)
class ExecutionDecision:
    action: str
    allowed: bool
    reason: str


def authorize(action: str, approved: bool = False) -> ExecutionDecision:
    allowed = can_execute(action, approved=approved)
    if allowed:
        return ExecutionDecision(action, True, "authorized")
    return ExecutionDecision(action, False, "explicit_human_approval_required")
