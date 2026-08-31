"""Server-side commercial authority policy for Hamed AI."""
from dataclasses import dataclass, field
from enum import Enum
import os
import secrets
from datetime import datetime, timezone


class Risk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ApprovalRequest:
    action: str
    description: str
    value: float | None = None
    risk: Risk = Risk.HIGH
    token: str = ""
    approved: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not self.token:
            self.token = secrets.token_urlsafe(24)


AUTONOMOUS_ACTIONS = {
    "sale", "negotiate", "affiliate_marketing", "marketing",
    "website_service", "purchase", "payment",
}

BLOCKED_ACTIONS = {"transfer", "contract", "account_change", "irreversible"}


def _autonomous_mode() -> bool:
    return os.getenv("HAMED_AUTONOMOUS_MODE", "false").lower() == "true"


def _limit_for(action: str) -> float:
    if action == "purchase":
        return float(os.getenv("HAMED_MAX_PURCHASE_VALUE", "0"))
    if action == "payment":
        return float(os.getenv("HAMED_MAX_PAYMENT_VALUE", "0"))
    return float("inf")


def can_execute(action: str, approved: bool = False, value: float | None = None,
                risk: Risk = Risk.LOW) -> bool:
    # Explicit human approval is the final authorization for known high-impact actions.
    if approved:
        return action in AUTONOMOUS_ACTIONS or action in BLOCKED_ACTIONS
    if action in BLOCKED_ACTIONS:
        return False
    if action not in AUTONOMOUS_ACTIONS:
        return True
    if not _autonomous_mode():
        return False if action in {"purchase", "payment"} else True
    if risk == Risk.HIGH:
        return False
    if action in {"purchase", "payment"}:
        if value is None or value < 0:
            return False
        return value <= _limit_for(action)
    return True
