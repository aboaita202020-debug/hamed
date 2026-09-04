"""Safe adapters for Hamed's autonomous commercial execution.

Adapters produce auditable outbound intents. They never invent recipients,
credentials, payments, contracts, or irreversible actions.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Optional
import os


@dataclass(frozen=True)
class ActionIntent:
    channel: str
    action: str
    status: str
    recipient: Optional[str] = None
    payload: Optional[dict[str, Any]] = None
    reason: str = ""


class ExecutionAdapters:
    """Build executable intents while keeping external side effects bounded."""

    def __init__(self, outbox_dir: str = "data/outbox") -> None:
        self.outbox_dir = outbox_dir

    def contact(self, prospect: dict[str, Any], message: str) -> ActionIntent:
        recipient = prospect.get("contact") or prospect.get("telegram") or prospect.get("email")
        channel = "telegram" if prospect.get("telegram") else "email" if prospect.get("email") else "unknown"
        if not recipient:
            return ActionIntent(channel, "contact", "blocked", reason="missing verified recipient")
        if not message.strip():
            return ActionIntent(channel, "contact", "blocked", recipient, reason="empty message")
        return ActionIntent(channel, "contact", "ready", str(recipient), {"message": message}, "ready for configured delivery adapter")

    def prepare_payment(self, amount: float, currency: str = "EGP") -> ActionIntent:
        if amount <= 0:
            return ActionIntent("payment", "collect", "blocked", reason="invalid amount")
        max_payment = float(os.getenv("HAMED_MAX_PAYMENT_VALUE", "0"))
        if max_payment <= 0 or amount > max_payment:
            return ActionIntent("payment", "collect", "approval_required", reason="payment exceeds autonomous server limit")
        return ActionIntent("payment", "collect", "ready", payload={"amount": amount, "currency": currency}, reason="within configured payment limit")

    def prepare_purchase(self, amount: float, supplier: Optional[str] = None) -> ActionIntent:
        if amount <= 0:
            return ActionIntent("procurement", "purchase", "blocked", reason="invalid amount")
        max_purchase = float(os.getenv("HAMED_MAX_PURCHASE_VALUE", "0"))
        if max_purchase <= 0 or amount > max_purchase:
            return ActionIntent("procurement", "purchase", "approval_required", recipient=supplier, reason="purchase exceeds autonomous server limit")
        if not supplier:
            return ActionIntent("procurement", "purchase", "blocked", reason="missing supplier")
        return ActionIntent("procurement", "purchase", "ready", recipient=supplier, payload={"amount": amount}, reason="within configured purchase limit")

    def queue(self, intent: ActionIntent) -> dict[str, Any]:
        """Return an auditable queue record; delivery is handled by a configured integration."""
        return asdict(intent)
