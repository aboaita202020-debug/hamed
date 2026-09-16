"""Production-ready WhatsApp Cloud API adapter with opt-out protection.

Core business logic stays outside this module; this adapter only translates
Meta webhook payloads and sends verified outbound messages.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class IncomingMessage:
    sender_id: str
    text: str
    message_id: str


class WhatsAppAdapter:
    def __init__(self, access_token: str | None = None, phone_number_id: str | None = None,
                 api_version: str | None = None, timeout: float = 20.0) -> None:
        self.access_token = access_token or os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = phone_number_id or os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.api_version = api_version or os.getenv("WHATSAPP_API_VERSION", "v23.0")
        self.timeout = timeout
        self.auto_send = os.getenv("HAMED_AUTO_SEND_WHATSAPP", "false").lower() == "true"
        self._opted_out: set[str] = set()

    def parse_message(self, payload: dict[str, Any]) -> IncomingMessage:
        try:
            value = payload["entry"][0]["changes"][0]["value"]
            message = value["messages"][0]
            sender = str(message["from"])
            message_id = str(message["id"])
            text = str(message.get("text", {}).get("body", ""))
            if not text and message.get("type") == "button":
                text = str(message.get("button", {}).get("text", ""))
            if not text:
                text = f"[whatsapp:{message.get('type', 'unknown')}]"
            if text.strip().lower() in {"stop", "unsubscribe", "إلغاء", "الغاء", "توقف"}:
                self._opted_out.add(sender)
            return IncomingMessage(sender_id=sender, text=text, message_id=message_id)
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError("Invalid WhatsApp webhook payload") from exc

    def is_opted_out(self, recipient: str) -> bool:
        return str(recipient) in self._opted_out

    def opt_out(self, recipient: str) -> None:
        self._opted_out.add(str(recipient))

    def send_message(self, recipient: str, text: str) -> str:
        recipient = str(recipient)
        if self.is_opted_out(recipient):
            raise PermissionError("Recipient has opted out of WhatsApp messages")
        if not self.access_token or not self.phone_number_id:
            raise RuntimeError("WhatsApp Cloud API credentials are not configured")
        url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"},
            json={"messaging_product": "whatsapp", "to": recipient, "type": "text", "text": {"body": text}},
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        messages = data.get("messages") or []
        if not messages or not messages[0].get("id"):
            raise RuntimeError("WhatsApp API returned no message id")
        return str(messages[0]["id"])
