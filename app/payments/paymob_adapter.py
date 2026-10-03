"""Paymob adapter.

Credentials are read only from environment variables. No card data is handled
by Hamed. Paymob-hosted checkout collects payment details and sends a callback.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
from typing import Any, Mapping
from urllib.request import Request, urlopen

from .payment_engine import PaymentRequest, PaymentResult


HMAC_FIELDS = [
    "amount", "created_at", "currency", "error_occured", "has_parent_transaction",
    "id", "integration_id", "is_3d_secure", "is_auth", "is_capture", "is_refunded",
    "is_standalone_payment", "is_voided", "order", "owner", "pending",
    "source_data_pan", "source_data_sub_type", "source_data_type", "success",
]


class PaymobAdapter:
    def __init__(self) -> None:
        self.api_key = os.getenv("PAYMOB_API_KEY", "")
        self.public_key = os.getenv("PAYMOB_PUBLIC_KEY", "")
        self.hmac_secret = os.getenv("PAYMOB_HMAC_SECRET", "")
        self.integration_id = os.getenv("PAYMOB_INTEGRATION_ID", "")
        self.base_url = os.getenv("PAYMOB_BASE_URL", "https://accept.paymob.com")

    def create_checkout(self, request: PaymentRequest) -> PaymentResult:
        if not all([self.api_key, self.public_key, self.integration_id]):
            return PaymentResult(provider="paymob", status="not_configured")

        payload = {
            "amount": request.amount_minor,
            "currency": request.currency,
            "payment_methods": [int(self.integration_id)],
            "items": [{
                "name": request.description,
                "amount": request.amount_minor,
                "description": request.description,
                "quantity": 1,
            }],
            "billing_data": {
                "first_name": request.customer_name,
                "last_name": "Customer",
                "email": request.customer_email,
                "phone_number": request.customer_phone,
            },
            "customer": {
                "first_name": request.customer_name,
                "email": request.customer_email,
            },
            "extras": {"order_id": request.order_id},
        }
        body = json.dumps(payload).encode("utf-8")
        req = Request(
            f"{self.base_url}/v1/intention/",
            data=body,
            headers={
                "Authorization": f"Token {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
        client_secret = data["client_secret"]
        checkout = (
            f"{self.base_url}/unifiedcheckout/?publicKey={self.public_key}"
            f"&clientSecret={client_secret}"
        )
        return PaymentResult(
            provider="paymob",
            status="checkout_created",
            checkout_url=checkout,
            provider_reference=str(data.get("id", "")),
        )

    def verify_callback(self, payload: Mapping[str, Any], signature: str | None) -> bool:
        if not self.hmac_secret or not signature:
            return False
        obj = payload.get("obj", payload)

        def value(field: str) -> str:
            v: Any = obj.get(field)
            if v is None:
                return ""
            if isinstance(v, bool):
                return "true" if v else "false"
            if isinstance(v, dict) and "id" in v:
                return str(v["id"])
            if isinstance(v, dict):
                return json.dumps(v, separators=(",", ":"))
            return str(v)

        raw = "".join(value(field) for field in HMAC_FIELDS)
        digest = hmac.new(
            self.hmac_secret.encode("utf-8"), raw.encode("utf-8"), hashlib.sha512
        ).hexdigest()
        return hmac.compare_digest(digest, signature)
