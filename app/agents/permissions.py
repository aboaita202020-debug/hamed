"""Server-side permission and approval primitives."""
from dataclasses import dataclass
from enum import Enum
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
    created_at: datetime = datetime.now(timezone.utc)

    def __post_init__(self) -> None:
        if not self.token:
            self.token = secrets.token_urlsafe(24)


def can_execute(action: str, approved: bool = False) -> bool:
    if action in {"purchase", "payment", "transfer", "contract", "publish", "account_change", "irreversible"}:
        return approved
    return True
