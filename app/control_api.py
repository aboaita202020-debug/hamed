"""Authenticated control channel for the ORVIA/HAMED AGI service."""
from __future__ import annotations
import hmac
import os
from fastapi import HTTPException

def require_control_secret(provided: str | None) -> None:
    expected = os.getenv("HAMED_CONTROL_SECRET", "").strip()
    if not expected:
        try:
            with open("data/control_secret", "r", encoding="utf-8") as fh:
                expected = fh.read().strip()
        except OSError:
            expected = ""
    if not expected:
        raise HTTPException(status_code=503, detail="Control secret is not configured")
    if not provided or not hmac.compare_digest(provided, expected):
        raise HTTPException(status_code=401, detail="Invalid control secret")

def tail_log(source: str = "server", limit: int = 100) -> list[str]:
    files = {
        "server": "data/hamed_server.log",
        "backend": "data/backend_out.log",
        "runner": "data/runner_live.log",
    }
    target = files.get(source, files["server"])
    try:
        with open(target, "r", encoding="utf-8", errors="replace") as fh:
            return fh.readlines()[-max(1, min(limit, 200)):]
    except OSError:
        return []
