"""Small approval-aware workflow primitives for Hamed."""
from dataclasses import dataclass
from .permissions import ApprovalRequest, can_execute


@dataclass
class PendingAction:
    action: str
    description: str
    value: float | None = None
    approval: ApprovalRequest | None = None


def prepare_action(action: str, description: str, value: float | None = None) -> PendingAction:
    if can_execute(action, approved=False):
        return PendingAction(action, description, value)
    return PendingAction(action, description, value, ApprovalRequest(action=action, description=description, value=value))


def execute_approved(pending: PendingAction) -> bool:
    return can_execute(pending.action, approved=bool(pending.approval and pending.approval.approved))
