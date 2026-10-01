"""InstaPay payment option for Hamed AI.

This adapter models customer-initiated bank transfers. It deliberately does
not claim a transfer is paid from a screenshot or customer message alone.
Production auto-confirmation requires an approved bank/payment integration.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class InstaPayConfig:
    receiving_identifier: str
    account_name: str
    currency: str = "EGP"


class InstaPayAdapter:
    provider = "instapay"

    def __init__(self, config: InstaPayConfig) -> None:
        self.config = config

    def payment_instructions(self, order_id: str, amount_egp: int) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "status": "awaiting_customer_transfer",
            "order_id": order_id,
            "amount": amount_egp,
            "currency": self.config.currency,
            "receiving_identifier": self.config.receiving_identifier,
            "account_name": self.config.account_name,
            "note": "Transfer through the official InstaPay app. Do not send a PIN or OTP to Hamed.",
        }

    def verify_callback(self, payload: Mapping[str, Any], signature: str | None = None) -> bool:
        """Only accept a future authenticated provider callback.

        InstaPay consumer transfers do not provide Hamed with a public webhook
        merely because a customer reports a transfer, so manual verification or
        an approved integration is required before marking an order PAID.
        """
        return bool(payload.get("authenticated_provider_callback")) and bool(signature)
