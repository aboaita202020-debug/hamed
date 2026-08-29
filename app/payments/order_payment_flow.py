"""Order-to-payment orchestration for Hamed AI.

Keeps payment selection separate from fulfillment and requires verified payment
before a paid order can be released for service execution.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4

from .payment_options import PaymentOption, egypt_payment_options, get_payment_option


class PaymentStatus(str, Enum):
    CREATED = "created"
    AWAITING_PAYMENT = "awaiting_payment"
    PAYMENT_REPORTED = "payment_reported"
    PAID = "paid"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class PaymentOrder:
    order_id: str
    customer_id: str
    amount: int
    currency: str
    status: PaymentStatus = PaymentStatus.CREATED
    selected_method: str | None = None
    provider_reference: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class PaymentOrderFlow:
    def __init__(self) -> None:
        self.orders: dict[str, PaymentOrder] = {}

    def create_order(self, customer_id: str, amount: int, currency: str = "EGP") -> PaymentOrder:
        if amount <= 0:
            raise ValueError("amount must be positive")
        order = PaymentOrder(str(uuid4()), customer_id, amount, currency)
        self.orders[order.order_id] = order
        return order

    def available_methods(self, country: str = "EG") -> list[PaymentOption]:
        if country.upper() == "EG":
            return egypt_payment_options()
        return []

    def select_method(self, order_id: str, method: str) -> PaymentOrder:
        order = self.orders[order_id]
        option = get_payment_option(method)  # validates the method
        if option.currency != order.currency:
            raise ValueError("payment method currency does not match order currency")
        order.selected_method = method
        order.status = PaymentStatus.AWAITING_PAYMENT
        order.provider_reference = f"HAMED-{order.order_id[:8].upper()}"
        return order

    def mark_paid(self, order_id: str, authenticated: bool) -> PaymentOrder:
        """Release an order only after an authenticated payment confirmation."""
        if not authenticated:
            raise PermissionError("authenticated payment confirmation is required")
        order = self.orders[order_id]
        order.status = PaymentStatus.PAID
        return order

    def can_start_fulfillment(self, order_id: str) -> bool:
        return self.orders[order_id].status is PaymentStatus.PAID
