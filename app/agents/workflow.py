"""Approval-aware end-to-end commercial workflow for Hamed."""
from dataclasses import dataclass
from enum import Enum
from .permissions import ApprovalRequest, can_execute


class Stage(str, Enum):
    REQUEST = "request"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    RECOMMENDATION = "recommendation"
    APPROVAL = "approval"
    EXECUTION = "execution"
    COMPLETE = "complete"


@dataclass
class PendingAction:
    action: str
    description: str
    value: float | None = None
    approval: ApprovalRequest | None = None
    stage: Stage = Stage.REQUEST


def prepare_action(action: str, description: str, value: float | None = None) -> PendingAction:
    if can_execute(action, approved=False):
        return PendingAction(action, description, value, stage=Stage.EXECUTION)
    return PendingAction(
        action,
        description,
        value,
        ApprovalRequest(action=action, description=description, value=value),
        Stage.APPROVAL,
    )


def approve_action(pending: PendingAction) -> None:
    if pending.approval is None:
        raise ValueError("This action does not require approval")
    pending.approval.approved = True
    pending.stage = Stage.EXECUTION


def execute_approved(pending: PendingAction) -> bool:
    allowed = can_execute(
        pending.action,
        approved=bool(pending.approval and pending.approval.approved),
    )
    if allowed:
        pending.stage = Stage.COMPLETE
    return allowed
