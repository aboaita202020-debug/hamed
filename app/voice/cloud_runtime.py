"""Cloud-first runtime helpers for Hamed Voice.

Hamed is designed to run on a server/cloud host rather than on the owner's phone
or desktop. The owner's device is only a control surface; outbound calls and
Twilio webhooks continue to work while that device is offline.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CloudRuntimeConfig:
    public_base_url: str
    environment: str = "production"
    require_https: bool = True

    @classmethod
    def from_env(cls) -> "CloudRuntimeConfig":
        url = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")
        if not url:
            raise RuntimeError("PUBLIC_BASE_URL is required for cloud voice runtime")
        if os.environ.get("HAMED_ALLOW_INSECURE_HTTP", "false").lower() != "true" and not url.startswith("https://"):
            raise RuntimeError("PUBLIC_BASE_URL must use HTTPS in production")
        return cls(public_base_url=url, environment=os.environ.get("HAMED_ENV", "production"))


def runtime_health() -> dict[str, Any]:
    """Return non-secret runtime status for monitoring/control dashboards."""
    return {
        "runtime": "cloud",
        "environment": os.environ.get("HAMED_ENV", "production"),
        "phone_independent": True,
        "twilio_configured": all(
            os.environ.get(key)
            for key in ("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_FROM_NUMBER")
        ),
        "openai_configured": bool(os.environ.get("OPENAI_API_KEY")),
        "public_base_url_configured": bool(os.environ.get("PUBLIC_BASE_URL")),
    }
