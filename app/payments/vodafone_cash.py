"""Vodafone Cash payment adapter for Hamed AI.

This adapter intentionally does not ask customers for wallet PINs, OTPs, or
card credentials. It creates a merchant payment instruction that can be
confirmed only after the merchant-side transaction is verified.

The adapter supports a safe manual/merchant-wallet flow. A direct automated
Vodafone Cash checkout should only be enabled after Vodafone provides the
appropriate merchant/API integration credentials and webhook contract.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
import secrets
from typing import Any, Mapping


@dataclass(frozen=True)
class VodafoneCashPayment:
    order_id: str
    amount_egp: int
    merchant_wallet: str
    reference: str
    instructions: str
    status: str = "pending_confirmation"


class VodafoneCashAdapter:
    provider = "vodafone_cash"

    def __init__(self, merchant_wallet: str | None = None) -> None:
        self.merchant_wallet = merchant_wallet or os.getenv("HAMED_VODAFONE_CASH_WALLET", "")

    def create_payment(self, order_id: str, amount_egp: int) -> VodafoneCashPayment:
        if amount_egp <= 0:
            raise ValueError("amount_egp must be greater than zero")
        if not self.merchant_wallet:
            raise ValueError("HAMED_VODAFONE_CASH_WALLET is not configured")

        reference = f"HAMED-{order_id}-{secrets.token_hex(4).upper()}"
        instructions = (
            f"حوّل {amount_egp} جنيه إلى محفظة Vodafone Cash التجارية {self.merchant_wallet}. "
            f"اكتب رقم المرجع {reference} في وصف/ملاحظة التحويل إن كان متاحًا، ثم أرسل إثبات الدفع. "
            "لن يطلب منك Hamed الرقم السري للمحفظة أو OTP."
        )
        return VodafoneCashPayment(
            order_id=order_id,
            amount_egp=amount_egp,
            merchant_wallet=self.merchant_wallet,
            reference=reference,
            instructions=instructions,
        )

    def confirm_verified_payment(
        self,
        payment: VodafoneCashPayment,
        verified_amount_egp: int,
        verified_reference: str,
    ) -> bool:
        """Confirm only after a trusted merchant/operator verification step."""
        return (
            verified_amount_egp == payment.amount_egp
            and verified_reference == payment.reference
        )

    def parse_verification(self, payload: Mapping[str, Any]) -> tuple[int, str] | None:
        """Parse an internally verified transaction record; not a public webhook."""
        try:
            return int(payload["amount_egp"]), str(payload["reference"])
        except (KeyError, TypeError, ValueError):
            return None
