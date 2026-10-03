"""
AIProviderRouter — spec section 16: model routing, fallback, cost logging,
no dependence on a single provider.

Concrete providers (OpenAI/Claude/DeepSeek/Mistral SDKs) are intentionally
NOT hard-imported here — that would force everyone to `pip install` every
SDK just to boot Core. Instead, wire real provider objects in at startup
(see scripts/run_server.py) via `router.register(provider)`.
"""
from __future__ import annotations

from typing import Optional

from app.config import settings
from app.logging_config import get_logger
from .base_provider import BaseAIProvider, AIResponse

logger = get_logger(__name__)


class AIProviderRouter:
    def __init__(self, default_provider: Optional[str] = None):
        self._providers: dict[str, BaseAIProvider] = {}
        self.default_provider = default_provider or settings.default_ai_provider
        self.total_cost_usd: float = 0.0

    def register(self, provider: BaseAIProvider) -> None:
        self._providers[provider.name] = provider

    def configured_providers(self) -> list[str]:
        return [name for name, p in self._providers.items() if p.is_configured()]

    def complete(self, prompt: str, system: Optional[str] = None,
                 preferred: Optional[str] = None) -> AIResponse:
        """Try the preferred/default provider first, then fall back to any
        other configured provider in registration order."""
        order = [preferred or self.default_provider] + [
            n for n in self._providers if n != (preferred or self.default_provider)
        ]

        last_error = "no_ai_provider_configured"
        for name in order:
            provider = self._providers.get(name)
            if not provider or not provider.is_configured():
                continue
            response = provider.complete(prompt, system=system)
            if response.success:
                self.total_cost_usd += response.cost_estimate_usd
                return response
            last_error = response.error
            logger.warning("Provider '%s' failed, trying next: %s", name, last_error)

        return AIResponse(success=False, error=last_error)
