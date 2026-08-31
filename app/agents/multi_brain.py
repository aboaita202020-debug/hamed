"""Multi-model brain router for Hamed AI."""
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
            model=self.model, max_tokens=4096,
            system=system or "You are Hamed AI, a reliable commercial AI agent.",
            messages=[m for m in messages if m.get("role") in {"user", "assistant"}],
        )
        return "".join(getattr(block, "text", "") for block in response.content).strip()

    def web_research(self, query: str, *, system: str = "") -> str:
        return self.generate_response([{"role": "user", "content": query}], system=system)


class OpenAICompatibleProvider:
    """Provider for APIs exposing an OpenAI-compatible /chat/completions endpoint."""
    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self.api_key, self.base_url, self.model = api_key, base_url.rstrip("/"), model

    def _call(self, messages: list[dict[str, str]], system: str = "") -> str:
        import requests
        payload_messages = ([{"role": "system", "content": system}] if system else []) + messages
        response = requests.post(
            self.base_url + "/chat/completions",
            headers={"Authorization": "Bearer " + self.api_key, "Content-Type": "application/json"},
            json={"model": self.model, "messages": payload_messages, "temperature": 0.2}, timeout=90,
        )
        response.raise_for_status()
        return str(response.json()["choices"][0]["message"]["content"]).strip()

    def generate_response(self, messages: list[dict[str, str]], *, system: str = "") -> str:
        return self._call(messages, system)

    def web_research(self, query: str, *, system: str = "") -> str:
        return self._call([{"role": "user", "content": query}], system)


class MultiBrainRouter:
    """Fallback or council routing across every configured Hamed brain."""
    def __init__(self, providers: list[tuple[str, AIProvider]], mode: str = "fallback") -> None:
        self.providers, self.mode = providers, mode
        if not providers:
            raise RuntimeError("No AI provider configured. Add at least one provider API key.")

    @property
    def provider_names(self) -> list[str]:
        return [name for name, _ in self.providers]

    def generate_response(self, messages: list[dict[str, str]], *, system: str = "") -> str:
        if self.mode == "council" and len(self.providers) > 1:
            answers = []
            for name, provider in self.providers:
                try: answers.append((name, provider.generate_response(messages, system=system)))
                except Exception: logger.exception("Provider %s failed in council mode", name)
            if len(answers) > 1:
                evidence = "\n\n".join("[%s]\n%s" % item for item in answers)
                synth = (system + "\n\n" if system else "") + "Synthesize these candidate answers into one decisive, factual answer. Do not invent facts.\n" + evidence
                try: return self.providers[0][1].generate_response(messages, system=synth)
                except Exception: return answers[0][1]
            if answers: return answers[0][1]
        last_error = None
        for name, provider in self.providers:
            try: return provider.generate_response(messages, system=system)
            except Exception as exc:
                last_error = exc; logger.exception("Provider %s failed; trying next", name)
        raise RuntimeError("All configured AI providers failed") from last_error

    def web_research(self, query: str, *, system: str = "") -> str:
        for name, provider in self.providers:
            try: return provider.web_research(query, system=system)
            except Exception: logger.exception("Research provider %s failed; trying next", name)
        raise RuntimeError("All configured AI research providers failed")


def build_brain_router(settings: Any) -> MultiBrainRouter:
    def get(name: str, default: Any = None) -> Any:
        value = getattr(settings, name, None)
        return value if value is not None else os.getenv(name.upper(), default)

    providers: list[tuple[str, AIProvider]] = []
    if get("openai_api_key"):
        providers.append(("openai", OpenAIProvider(get("openai_api_key"), get("openai_model", "gpt-5"))))
    if get("anthropic_api_key"):
        providers.append(("claude", AnthropicProvider(get("anthropic_api_key"), get("anthropic_model", "claude-sonnet-4-5"))))
    if get("deepseek_api_key"):
        providers.append(("deepseek", OpenAICompatibleProvider(get("deepseek_api_key"), get("deepseek_base_url", "https://api.deepseek.com"), get("deepseek_model", "deepseek-chat"))))
    if get("kimi_api_key"):
        providers.append(("kimi", OpenAICompatibleProvider(get("kimi_api_key"), get("kimi_base_url", "https://api.moonshot.cn/v1"), get("kimi_model", "kimi-k2.5"))))

    requested = [x.strip().lower() for x in os.getenv("HAMED_AI_PROVIDERS", "openai,claude,deepseek,kimi").split(",") if x.strip()]
    ordered = [item for key in requested for item in providers if item[0] == key]
    return MultiBrainRouter(ordered or providers, mode=os.getenv("HAMED_AI_MODE", "fallback").lower())
