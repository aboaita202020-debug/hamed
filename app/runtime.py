"""Shared HTTP listener configuration for Hamed runtime entrypoints."""
from __future__ import annotations

import os


def http_host() -> str:
    """Return the public bind host configured for Hamed."""
    return os.getenv("HAMED_HOST", "0.0.0.0")


def http_port() -> int:
    """Return Hamed's explicit port, or the platform-provided ``PORT`` value."""
    value = os.getenv("HAMED_PORT", os.getenv("PORT", "8000"))
    try:
        port = int(value)
    except ValueError as exc:
        raise ValueError("HAMED_PORT or PORT must be an integer") from exc
    if not 1 <= port <= 65535:
        raise ValueError("HAMED_PORT or PORT must be between 1 and 65535")
    return port
