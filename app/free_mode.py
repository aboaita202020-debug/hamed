"""Free-first runtime policy for Hamed.

Keeps core research, auditing, planning and learning local/open-source where possible.
Paid APIs are opt-in and disabled by default.
"""
import os


FREE_MODE = os.getenv("HAMED_FREE_MODE", "true").lower() in {"1", "true", "yes", "on"}
PAID_APIS_ENABLED = os.getenv("HAMED_ENABLE_PAID_APIS", "false").lower() in {"1", "true", "yes", "on"}


def allow_paid_api() -> bool:
    """Return whether Hamed may use a paid external API."""
    return (not FREE_MODE) and PAID_APIS_ENABLED


def provider_mode() -> str:
    return "free-first" if FREE_MODE else "paid-enabled"
