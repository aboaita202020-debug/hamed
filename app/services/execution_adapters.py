"""Safe adapters for Hamed's autonomous commercial execution.

Adapters produce auditable outbound intents and can optionally deliver Telegram
or WhatsApp messages when the recipient is explicitly verified/configured.
They never invent recipients, credentials, payments, contracts, or irreversible actions.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Optional
import json
import os
import urllib.parse
import urllib.request


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
        recipient = (
            prospect.get("telegram_chat_id")
            or prospect.get("telegram")
            or prospect.get("whatsapp")
            or prospect.get("email")
        )
        if prospect.get("telegram_chat_id") or prospect.get("telegram"):
            channel = "telegram"
        elif prospect.get("whatsapp"):
            channel = "whatsapp"
        elif prospect.get("email"):
            channel = "email"
        else:
            channel = "unknown"
        if not recipient:
            return ActionIntent(channel, "contact", "blocked", reason="missing verified recipient")
        if not prospect.get("verified_contact", False):
            return ActionIntent(channel, "contact", "blocked", str(recipient), reason="recipient is not explicitly verified")
        if prospect.get("opted_out", False):
            return ActionIntent(channel, "contact", "blocked", str(recipient), reason="recipient opted out")
        if not message.strip():
            return ActionIntent(channel, "contact", "blocked", str(recipient), reason="empty message")
        return ActionIntent(channel, "contact", "ready", str(recipient), {"message": message}, "ready for configured delivery adapter")

    def send_telegram(self, prospect: dict[str, Any], message: str) -> ActionIntent:
        intent = self.contact(prospect, message)
        if intent.status != "ready" or intent.channel != "telegram":
            return intent
        if os.getenv("HAMED_AUTO_SEND_TELEGRAM", "false").lower() != "true":
            return intent
        token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        if not token:
            return ActionIntent("telegram", "contact", "blocked", intent.recipient, reason="TELEGRAM_BOT_TOKEN is not configured")
        try:
            data = urllib.parse.urlencode({"chat_id": str(intent.recipient), "text": message}).encode("utf-8")
            request = urllib.request.Request(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data=data,
                method="POST",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            with urllib.request.urlopen(request, timeout=15) as response:
                body = json.loads(response.read().decode("utf-8"))
            if body.get("ok"):
                return ActionIntent("telegram", "contact", "sent", intent.recipient, {"message": message}, "Telegram delivery succeeded")
            return ActionIntent("telegram", "contact", "error", intent.recipient, reason="Telegram API rejected message")
        except Exception as exc:
            return ActionIntent("telegram", "contact", "error", intent.recipient, reason=type(exc).__name__)

    def send_whatsapp(self, prospect: dict[str, Any], message: str) -> ActionIntent:
        """Send a WhatsApp Cloud API text message only when explicitly enabled.

        The business phone number itself is configured as HAMED_WHATSAPP_NUMBER
        for identity/display. Delivery requires Meta's PHONE_NUMBER_ID and access
        token in secrets; the customer's WhatsApp number comes from the prospect.
        """
        intent = self.contact(prospect, message)
        if intent.status != "ready" or intent.channel != "whatsapp":
            return intent
        if os.getenv("HAMED_AUTO_SEND_WHATSAPP", "false").lower() != "true":
            return intent

        token = os.getenv("WHATSAPP_ACCESS_TOKEN", "").strip()
        phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "").strip()
        graph_version = os.getenv("WHATSAPP_GRAPH_VERSION", "v23.0").strip()
        if not token:
            return ActionIntent("whatsapp", "contact", "blocked", intent.recipient, reason="WHATSAPP_ACCESS_TOKEN is not configured")
        if not phone_number_id:
            return ActionIntent("whatsapp", "contact", "blocked", intent.recipient, reason="WHATSAPP_PHONE_NUMBER_ID is not configured")

        recipient = str(intent.recipient).replace("+", "").replace(" ", "").replace("-", "")
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": message},
        }).encode("utf-8")
        request = urllib.request.Request(
            f"https://graph.facebook.com/{graph_version}/{phone_number_id}/messages",
            data=payload,
            method="POST",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                body = json.loads(response.read().decode("utf-8"))
            if body.get("messages"):
                return ActionIntent("whatsapp", "contact", "sent", intent.recipient, {"message": message}, "WhatsApp delivery succeeded")
            return ActionIntent("whatsapp", "contact", "error", intent.recipient, reason="WhatsApp API rejected message")
        except Exception as exc:
            return ActionIntent("whatsapp", "contact", "error", intent.recipient, reason=type(exc).__name__)

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
