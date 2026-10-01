"""
Permission Layer / Approval Gate — spec section 13 & 27.

Every sensitive action (a Tool call, a payment, a purchase, a big
discount, signing a contract) MUST pass through here before it runs.
The layer:
  1. Decides AUTO / DENIED / PENDING_APPROVAL based on configured limits.
  2. Writes an Audit Log entry no matter what the decision is
     (actor, timestamp, action, reason, input, result, permission —
     exactly the fields required by the spec).

Nothing in this file changes its own limits at runtime — the spec
explicitly forbids the system from altering its own permissions
(section 28: "لا يغير صلاحياته بنفسه").
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from app.config import ApprovalLimits, settings
from app.db.repository import Repository
from app.db.models import AuditLogEntry
from app.logging_config import get_logger

logger = get_logger(__name__)


class PermissionDecision(str, Enum):
    AUTO = "AUTO"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    PENDING_APPROVAL = "PENDING_APPROVAL"


class ApprovalRequired(Exception):
    """Raised when an action needs a human decision before it can run."""

    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason
        super().__init__(f"Approval required for '{action}': {reason}")


@dataclass
class PermissionCheck:
    action: str
    amount_egp: float = 0.0
    discount_pct: float = 0.0
    is_contract: bool = False
    high_impact: bool = False


class PermissionLayer:
    """Central gate every Agent/Tool call goes through."""

    # Actions that never need money-based checks and are always allowed
    # automatically (spec section 13: "مسموح تلقائيًا").
    ALWAYS_AUTO_ACTIONS = {
        "web_research",
        "analyze_data",
        "rank_opportunities",
        "generate_lead",
        "draft_proposal",
        "update_crm",
        "send_followup",
        "fact_check",
    }

    def __init__(self, repository: Repository, limits: Optional[ApprovalLimits] = None):
        self.repo = repository
        self.limits = limits or settings.approval_limits

    def evaluate(self, check: PermissionCheck) -> PermissionDecision:
        if check.action in self.ALWAYS_AUTO_ACTIONS and not check.high_impact:
            return PermissionDecision.AUTO

        if check.is_contract and self.limits.require_approval_for_contracts:
            return PermissionDecision.PENDING_APPROVAL

        if check.high_impact:
            return PermissionDecision.PENDING_APPROVAL

        if check.discount_pct and check.discount_pct > self.limits.max_auto_discount_pct:
            return PermissionDecision.PENDING_APPROVAL

        if check.amount_egp and check.action == "purchase" and \
                check.amount_egp > self.limits.max_auto_purchase_egp:
            return PermissionDecision.PENDING_APPROVAL

        if check.amount_egp and check.action == "payment" and \
                check.amount_egp > self.limits.max_auto_payment_egp:
            return PermissionDecision.PENDING_APPROVAL

        return PermissionDecision.AUTO

    def authorize(
        self,
        actor: str,
        check: PermissionCheck,
        reason: str = "",
        input_data: Any = None,
    ) -> PermissionDecision:
        """Evaluate + write an Audit Log entry. Raises ApprovalRequired
        if the action cannot proceed automatically, so callers (Agents)
        are forced to handle the human-in-the-loop path explicitly."""
        decision = self.evaluate(check)

        self.repo.write_audit_log(
            AuditLogEntry(
                actor=actor,
                action=check.action,
                permission=decision.value,
                reason=reason,
                input_data=input_data,
                result="pending" if decision == PermissionDecision.PENDING_APPROVAL else "authorized",
            )
        )

        if decision == PermissionDecision.PENDING_APPROVAL:
            logger.info("Action '%s' by '%s' requires human approval.", check.action, actor)
            raise ApprovalRequired(check.action, reason or "exceeds auto-approval limits")

        if decision == PermissionDecision.DENIED:
            logger.warning("Action '%s' by '%s' was DENIED.", check.action, actor)

        return decision

    def record_manual_approval(self, actor: str, action: str, approved_by: str) -> None:
        """Called by the human owner (e.g. via Telegram command) to unblock
        a PENDING_APPROVAL action. Always audited."""
        self.repo.write_audit_log(
            AuditLogEntry(
                actor=actor,
                action=action,
                permission=PermissionDecision.APPROVED.value,
                reason=f"manually approved by {approved_by}",
            )
        )
