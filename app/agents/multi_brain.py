"""Multi-model brain router for Hamed AI.

Providers are optional and are enabled only when their environment key exists.
The router keeps the common AIProvider interface so existing agents do not change.
"""
from __future__ import annotations

import logging
import os
from typing import Any

from .provider import AIProvider, OpenAIProvider

logger = logging.getLogger(__name__)


class AnthropicProvider:
    def __init__(self, api_key: str, model: str) -> None:
        from anthropic import Anthropic
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate_response(self, messages: list[dict[str, str]], *, system: str = "") -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system or "You are Hamed AI, a reliable commercial AI agent.",
            messages=[m for m in messages if m.get("role") in {"user", "assistant"}],
        )
        parts = [getattr(block, "text", "") for block in response.content]
        return "".join(parts).strip()

    def web_research(self, query: str, *, system: str = "") -> str:
        return self.generate_response([{"role": "user", "content": query}], system=system)


class OpenAICompatibleProvider:
    """Provider for APIs exposing an OpenAI-compatible /chat/completions endpoint."""
    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    def _call(self, messages: list[dict[str, str]], system: str = "") -> str:
        import requests
        payload_messages = []
        if system:
            payload_messages.append({"role": "system", "content": system})
        payload_messages.extend(messages)
        response = requests.post(
            self.base_url + "/chat/completions",
            headers={"Authorization": "Bearer " + self.api_key, "Content-Type": "application/json"},
            json={"model": self.model, "messages": payload_messages, "temperature": 0.2},
            timeout=90,
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return str(data["choices"][0]["message"]["content"]).strip()

    def generate_response(self, messages: list[dict[str, str]], *, system: str = "") -> str:
        return self._call(messages, system)

    def web_research(self, query: str, *, system: str = "") -> str:
        return self._call([{"role": "user", "content": query}], system)


class MultiBrainRouter:
    """Routes Hamed requests across configured models with automatic fallback.

    Modes:
      - fallback: try providers in configured order until one succeeds.
      - council: ask all configured providers, then synthesize with the first provider.
    """
    def __init__(self, providers: list[tuple[str, AIProvider]], mode: str = "fallback") -> None:
        self.providers = providers
        self.mode = mode
        if not providers:
            raise RuntimeError("No AI provider configured. Add at least one provider API key.")

    @property
    def provider_names(self) -> list[str]:
        return [name for name, _ in self.providers]

    def generate_response(self, messages: list[dict[str, str]], *, system: str = "") -> str:
        if self.mode == "council" and len(self.providers) > 1:
            answers = []
            for name, provider in self.providers:
                try:
                    answers.append((name, provider.generate_response(messages, system=system)))
                except Exception:
                    logger.exception("Provider %s failed in council mode", name)
            if answers:
                if len(answers) == 1:
                    return answers[0][1]
                evidence = "\n\n".join("[%s]\n%s" % item for item in answers)
                synth_system = (system + "\n\n" if system else "") + (
                    "You are the lead Hamed brain. Synthesize the candidate answers below. "
                    "Resolve contradictions conservatively, do not invent facts, and return one decisive answer.\n"
                    + evidence
                )
                try:
                    return self.providers[0][1].generate_response(messages, system=synth_system)
                except Exception:
                    return answers[0][1]
        last_error: Exception | None = None
        for name, provider in self.providers:
            try:
                return provider.generate_response(messages, system=system)
            except Exception as exc:
                last_error = exc
                logger.exception("Provider %s failed; trying next provider", name)
        raise RuntimeError("All configured AI providers failed") from last_error

    def web_research(self, query: str, *, system: str = "") -> str:
        for name, provider in self.providers:
            try:
                return provider.web_research(query, system=system)
            except Exception:
                logger.exception("Research provider %s failed; trying next provider", name)
        raise RuntimeError("All configured AI research providers failed")


def build_brain_router(settings: Any) -> MultiBrainRouter:
    providers: list[tuple[str, AIProvider]] = []
    if settings.openai_api_key:
        providers.append(("openai", OpenAIProvider(settings.openai_api_key, settings.openai_model)))
    if settings.anthropic_api_key:
        providers.append(("claude", AnthropicProvider(settings.anthropic_api_key, settings.anthropic_model)))
    if settings.deepseek_api_key:
        providers.append(("deepseek", OpenAICompatibleProvider(settings.deepseek_api_key, settings.deepseek_base_url, settings.deepseek_model)))
    if settings.kimi_api_key:
        providers.append(("kimi", OpenAICompatibleProvider(settings.kimi_api_key, settings.kimi_base_url, settings.kimi_model)))

    requested = [x.strip().lower() for x in os.getenv("HAMED_AI_PROVIDERS", "openai,claude,deepseek,kimi").split(",") if x.strip()]
    ordered = [item for key in requested for item in providers if item[0] == key]
    if not ordered:
        ordered = providers
    return MultiBrainRouter(ordered, mode=os.getenv("HAMED_AI_MODE", "fallback").lower())
