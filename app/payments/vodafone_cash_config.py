"""Deployment-safe configuration for Vodafone Cash receiving details.

The real wallet number must be supplied through the VODAFONE_CASH_RECEIVING_NUMBER
environment variable and must never be committed to source control.
"""
from __future__ import annotations

import os


def get_vodafone_cash_receiving_number() -> str:
    number = os.getenv("VODAFONE_CASH_RECEIVING_NUMBER", "").strip()
    if not number:
        raise RuntimeError("VODAFONE_CASH_RECEIVING_NUMBER is not configured")
    return number
