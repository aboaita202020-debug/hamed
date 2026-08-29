"""Payment orchestration for Hamed AI.

Free-first: no payment provider is called unless explicitly configured.
The engine creates payment intents/links through an adapter and only marks
an order paid after a verified provider callback.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any, Mapping, Protocol


@dataclass(frozen=True)
class PaymentRequest:
    order_id: str
    amount_minor: int
    currency: str
    customer_name: str
    customer_email: str
    customer_phone: str
    description: str


@dataclass(frozen=True)
class PaymentResult:
    provider: str
    status: str
    checkout_url: str | None = None
    provider_reference: str | None = None


class PaymentAdapter(Protocol):
    def create_checkout(self, request: PaymentRequest) -> PaymentResult: ...
    def verify_callback(self, payload: Mapping[str, Any], signature: str | None) -> bool: ...


class PaymentEngine:
    def __init__(self, adapter: PaymentAdapter | None = None) -> None:
        self.adapter = adapter

    @property
    def enabled(self) -> bool:
        return os.getenv("HAMED_PAYMENTS_ENABLED", "false").lower() == "true"

    @property
    def auto_spending(self) -> bool:
        return os.getenv("HAMED_AUTO_SPENDING", "false").lower() == "true"

    def create_checkout(self, request: PaymentRequest) -> PaymentResult:
        if not self.enabled or self.adapter is None:
            return PaymentResult(provider="none", status="disabled")
        return self.adapter.create_checkout(request)

    def accept_callback(self, payload: Mapping[str, Any], signature: str | None) -> bool:
        if not self.enabled or self.adapter is None:
            return False
        return self.adapter.verify_callback(payload, signature)


def build_default_engine() -> PaymentEngine:
    """Return a configured engine without importing or calling paid APIs by default."""
    return PaymentEngine(adapter=None)
