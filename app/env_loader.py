"""Minimal .env loader (standard library only).

Variables already present in the process environment always win, so real
environment settings (Koyeb/Oracle/systemd) are never overridden by a local file.
"""
from __future__ import annotations

import os
from pathlib import Path


def load_env(path: str | os.PathLike | None = None) -> int:
    """Load KEY=VALUE lines from .env into os.environ. Returns the number of variables set."""
    env_path = Path(path) if path else Path(__file__).resolve().parent.parent / ".env"
    if not env_path.is_file():
        return 0
    loaded = 0
    for raw in env_path.read_text(encoding="utf-8-sig", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key and value and key not in os.environ:
            os.environ[key] = value
            loaded += 1
    return loaded