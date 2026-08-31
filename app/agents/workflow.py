"""Commercial workflow with demo, deposit, and final-payment gates."""
from dataclasses import dataclass
from enum import Enum
from .permissions import ApprovalRequest, can_execute


class Stage(str, Enum):
    REQUEST = "request"
    DEMO = "demo"
    OFFER = "offer"
    WAITING_DEPOSIT = "waiting_deposit"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    RECOMMENDATION = "recommendation"
    APPROVAL = "approval"
    EXECUTION = "execution"
    COMPLETED_PENDING_PAYMENT = "completed_pending_payment"
    FINAL_DELIVERY = "final_delivery"
    COMPLETE = "complete"


@dataclass
class PendingAction:
    action: str
    description: str
    value: float | None = None
    approval: ApprovalRequest | None = None
    stage: Stage = Stage.REQUEST
    deposit_percent: float = 10.0
    deposit_verified: bool = False
    full_payment_verified: bool = False
    demo_delivered: bool = False


def prepare_action(action: str, description: str, value: float | None = None) -> PendingAction:
    pending = PendingAction(action, description, value)
    pending.stage = Stage.OFFER
    return pending


def mark_demo_delivered(pending: PendingAction) -> None:
    """Record a limited pre-payment demo; never treat it as final delivery."""
    pending.demo_delivered = True
    if not pending.deposit_verified:
        pending.stage = Stage.WAITING_DEPOSIT


def verify_deposit(pending: PendingAction, amount: float) -> bool:
    """Allow work to start only after >=10% of the agreed offer is verified."""
    if pending.value is None or pending.value <= 0:
        return False
    required = pending.value * (pending.deposit_percent / 100.0)
    if amount < required:
        return False
    pending.deposit_verified = True
    pending.stage = Stage.EXECUTION
    return True


def complete_work(pending: PendingAction) -> None:
    if not pending.deposit_verified:
        raise PermissionError("Cannot start or complete paid work before verified deposit")
    pending.stage = Stage.COMPLETED_PENDING_PAYMENT


def verify_full_payment(pending: PendingAction, amount: float) -> bool:
    """Verify that the full agreed amount has been received before final delivery."""
    if pending.value is None or amount < pending.value:
        return False
    pending.full_payment_verified = True
    pending.stage = Stage.FINAL_DELIVERY
    return True


def final_delivery_allowed(pending: PendingAction) -> bool:
    return pending.full_payment_verified


def approve_action(pending: PendingAction) -> None:
    if pending.approval is None:
        raise ValueError("This action does not require approval")
    pending.approval.approved = True
    pending.stage = Stage.EXECUTION


def execute_approved(pending: PendingAction) -> bool:
    """Legacy approval path; payment gates still apply to delivery-sensitive work."""
    allowed = can_execute(pending.action, approved=bool(pending.approval and pending.approval.approved))
    if allowed:
        pending.stage = Stage.COMPLETE
    return allowed
