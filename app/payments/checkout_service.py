"""Unified checkout service for Hamed AI payment methods."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .order_payment_flow import PaymentOrderFlow
from .payment_options import PaymentOption
from .vodafone_cash_config import get_vodafone_cash_receiving_number


@dataclass(frozen=True)
class Checkout:
    order_id: str
    reference: str
    method: str
    amount: int
    currency: str
    instructions: dict[str, Any]


class CheckoutService:
    def __init__(self, flow: PaymentOrderFlow | None = None) -> None:
        self.flow = flow or PaymentOrderFlow()

    def create_checkout(self, order_id: str, method: str) -> Checkout:
        order = self.flow.select_method(order_id, method)
        option: PaymentOption = next(
            item for item in self.flow.available_methods("EG") if item.method == method
        )
        instructions: dict[str, Any] = {"provider": method}
        if method == "vodafone_cash":
            instructions.update({
                "receiving_number": get_vodafone_cash_receiving_number(),
                "message": "حوّل المبلغ ثم أرسل مرجع العملية للتحقق.",
            })
        elif method == "instapay":
            instructions["message"] = "نفّذ التحويل عبر تطبيق InstaPay الرسمي ثم أرسل مرجع العملية للتحقق."
        elif method == "paymob":
            instructions["message"] = "سيتم إنشاء رابط Checkout عند تفعيل بيانات Paymob في بيئة التشغيل."
        return Checkout(
            order_id=order.order_id,
            reference=order.provider_reference or "",
            method=method,
            amount=order.amount,
            currency=order.currency,
            instructions=instructions,
        )
