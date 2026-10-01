"""HAMED central intelligence.

OpenAI is the system-level central brain. Other configured models form the
supporting council and are used only when the central provider is unavailable
or when the caller explicitly requests a council fallback.
"""
from __future__ import annotations

from .provider import MultiBrainProvider, OpenAIProvider


class CentralBrainProvider:
    """OpenAI-first provider with a multi-model council fallback."""

    def __init__(self, openai_api_key: str | None, openai_model: str = "gpt-5") -> None:
        self.central = OpenAIProvider(openai_api_key, openai_model) if openai_api_key else None
        try:
            self.council = MultiBrainProvider()
        except Exception:
            self.council = None

    @property
    def mode(self) -> str:
        if self.central:
            return "openai-central"
        if self.council:
            return "council-fallback"
        return "fallback"

    def generate_response(self, messages, *, system: str = "") -> str:
        errors: list[str] = []
        if self.central:
            try:
                result = self.central.generate_response(messages, system=system)
                if result:
                    return result
            except Exception as exc:
                errors.append("openai:" + type(exc).__name__)
        if self.council:
            try:
                result = self.council.generate_response(messages, system=system)
                if result:
                    return result
            except Exception as exc:
                errors.append("council:" + type(exc).__name__)
        raise RuntimeError("No AI brain available: " + ", ".join(errors))

    def web_research(self, query: str, *, system: str = "") -> str:
        errors: list[str] = []
        if self.central:
            try:
                result = self.central.web_research(query, system=system)
                if result:
                    return result
            except Exception as exc:
                errors.append("openai:" + type(exc).__name__)
        if self.council:
            try:
                result = self.council.web_research(query, system=system)
                if result:
                    return result
            except Exception as exc:
                errors.append("council:" + type(exc).__name__)
        raise RuntimeError("No AI research brain available: " + ", ".join(errors))

    def available_brains(self) -> list[str]:
        names = []
        if self.central:
            names.append("openai-central")
        if self.council:
            names.extend("council:" + name for name in self.council.available_brains())
        return names
