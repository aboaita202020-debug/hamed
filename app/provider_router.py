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


class FreeLLMAPIAdapter:
    name = "freellmapi"

    def state(self) -> ProviderState:
        configured = bool(os.getenv("FREELLMAPI_BASE_URL") and os.getenv("FREELLMAPI_API_KEY"))
        return ProviderState(
            self.name,
            configured,
            "configured" if configured else "offline",
            os.getenv("FREELLMAPI_MODEL", "default"),
        )

    def generate(self, prompt: str) -> str:
        from openai import OpenAI
        client = OpenAI(
            api_key=os.getenv("FREELLMAPI_API_KEY", "freellm-local"),
            base_url=os.getenv("FREELLMAPI_BASE_URL", "http://localhost:3001/v1"),
        )
        response = client.chat.completions.create(
            model=os.getenv("FREELLMAPI_MODEL", "auto"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=900,
        )
        return response.choices[0].message.content or ""


class SafeFallbackProvider:
    def __init__(self, name: str = "fallback") -> None:
        self.name = name

    def state(self) -> ProviderState:
        return ProviderState(self.name, False, "offline", "mock")

    def generate(self, prompt: str) -> str:
        topic = prompt.split("Current learning topic:", 1)[-1].strip().split("\n", 1)[0][:180]
        return (
            "HAMED_RULE_BASED_FALLBACK\n"
            f"Topic: {topic}\n"
            "Actionable opportunities: identify 5 prospects in this topic; for each, validate customer/problem/demand before outreach.\n"
            "Growth loop: research -> problem evidence -> offer -> prospect -> outreach -> CRM -> follow-up -> revenue.\n"
            "Constraints: evidence first; assumptions labeled; no invented companies, prices, credentials, or completed external actions.\n"
            "Next action: collect public evidence and create the first opportunity record."
        )


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
            "freellmapi": FreeLLMAPIAdapter(),
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
        result.append(self.providers["freellmapi"].state())
        return result

    def available(self) -> list[str]:
        return [s.name for s in self.states() if s.configured]

    def select(self, preferred: str | None = None) -> Provider:
        if preferred == "freellmapi" and self.providers["freellmapi"].state().configured:
            return self.providers["freellmapi"]
        if preferred == "openai" and openai_provider.check_connection()["connected"]:
            return self.providers["openai"]
        if openai_provider.check_connection()["connected"]:
            return self.providers["openai"]
        if self.providers["freellmapi"].state().configured:
            return self.providers["freellmapi"]
        return self.fallback

    def generate(self, prompt: str, preferred: str | None = None) -> str:
        candidates = ([preferred] if preferred else []) + ["openai", "freellmapi"]
        seen: set[str] = set()
        errors: list[str] = []
        for name in candidates:
            if not name or name in seen or name not in self.providers:
                continue
            seen.add(name)
            provider = self.providers[name]
            if not provider.state().configured:
                continue
            try:
                return provider.generate(prompt)
            except Exception as exc:
                errors.append(f"{name}:{type(exc).__name__}")
        if errors:
            return f"ORVIA_SAFE_FALLBACK: providers failed ({', '.join(errors)}); no external action was performed."
        return self.fallback.generate(prompt)

    def health(self) -> dict:
        states = self.states()
        connected = [s.name for s in states if s.mode == "connected"]
        configured = [s.name for s in states if s.configured]
        free_configured = [x["id"] for x in configured_free_sources()]
        return {
            "configured": configured,
            "connected": connected,
            "offline": [s.name for s in states if not s.configured],
            "active": connected[0] if connected else ("freellmapi" if "freellmapi" in configured else "fallback"),
            "free_ai_sources_configured": free_configured,
            "safe_fallback": not bool(connected or configured),
        }


provider_router = ProviderRouter()
