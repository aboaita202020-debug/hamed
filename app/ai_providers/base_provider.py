"""Base interface every AI provider adapter implements (spec section 16)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class AIResponse:
    success: bool
    text: str = ""
    provider: str = ""
    model: str = ""
    cost_estimate_usd: float = 0.0
    error: str = ""


class BaseAIProvider:
    name: str = "base"

    def is_configured(self) -> bool:  # pragma: no cover - interface
        raise NotImplementedError

    def complete(self, prompt: str, system: Optional[str] = None) -> AIResponse:  # pragma: no cover
        raise NotImplementedError
