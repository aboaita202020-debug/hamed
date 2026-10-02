from __future__ import annotations

import os
from dataclasses import dataclass
from typing import ClassVar, Protocol

from .providers import openai_provider
from .free_ai_scout import configured as configured_free_sources


@dataclass(frozen=True)
class ProviderState:
    name: str
    configured: bool
    mode: str
    model: str


class Provider(Protocol):
    name: str

    def state(self) -> ProviderState: ...
    def generate(self, prompt: str) -> str: ...


class SafeFallbackProvider:
    def __init__(self, name: str = "fallback") -> None:
        self.name = name

    def state(self) -> ProviderState:
        return ProviderState(self.name, False, "offline", "mock")

    def generate(self, prompt: str) -> str:
        return "ORVIA_SAFE_FALLBACK: no external model is configured; no external action was performed."


class OpenAIAdapter:
    name = "openai"

    def state(self) -> ProviderState:
        state = openai_provider.check_connection()
        mode = "connected" if state["connected"] else ("configured" if state["configured"] else "offline")
        return ProviderState(self.name, bool(state["configured"]), mode, state["model"])

    def generate(self, prompt: str) -> str:
        return openai_provider.generate(prompt).text


class ProviderRouter:
    ENV: ClassVar[dict[str, tuple[str, str]]] = {
        "openai": ("OPENAI_API_KEY", "OPENAI_MODEL"),
        "anthropic": ("ANTHROPIC_API_KEY", "ANTHROPIC_MODEL"),
        "gemini": ("GEMINI_API_KEY", "GEMINI_MODEL"),
        "deepseek": ("DEEPSEEK_API_KEY", "DEEPSEEK_MODEL"),
        "kimi": ("KIMI_API_KEY", "KIMI_MODEL"),
    }

    def __init__(self) -> None:
        self.fallback = SafeFallbackProvider()
        self.providers: dict[str, Provider] = {
            "openai": OpenAIAdapter(),
            "anthropic": SafeFallbackProvider("anthropic"),
            "gemini": SafeFallbackProvider("gemini"),
            "deepseek": SafeFallbackProvider("deepseek"),
            "kimi": SafeFallbackProvider("kimi"),
            "freellmapi": SafeFallbackProvider("freellmapi"),
        }

    def states(self) -> list[ProviderState]:
        result: list[ProviderState] = []
        for name, (key, model) in self.ENV.items():
            if name == "openai":
                result.append(self.providers[name].state())
            else:
                configured = bool(os.getenv(key))
                result.append(
                    ProviderState(
                        name,
                        configured,
                        "configured" if configured else "offline",
                        os.getenv(model) or "default",
                    )
                )
        return result

    def available(self) -> list[str]:
        return [s.name for s in self.states() if s.configured]

    def select(self, preferred: str | None = None) -> Provider:
        if preferred == "openai" and openai_provider.check_connection()["connected"]:
            return self.providers["openai"]
        if openai_provider.check_connection()["connected"]:
            return self.providers["openai"]
        return self.fallback

    def health(self) -> dict:
        states = self.states()
        connected = [s.name for s in states if s.mode == "connected"]
        configured = [s.name for s in states if s.configured]
        return {
            "configured": configured,
            "connected": connected,
            "offline": [s.name for s in states if not s.configured],
            "active": connected[0] if connected else ("freellmapi" if configured_free_sources() else "fallback"),
            "free_ai_sources_configured": [x["id"] for x in configured_free_sources()],
            "safe_fallback": not bool(connected or configured_free_sources()),
        }


provider_router = ProviderRouter()
