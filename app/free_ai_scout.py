from __future__ import annotations

"""Discoverable registry for free/zero-cost LLM sources.

The scout never creates accounts, bypasses quotas, or harvests API keys.
It records public sources and lets Hamed validate/configure them explicitly.
"""

from dataclasses import dataclass
from typing import Iterable
import os


@dataclass(frozen=True)
class FreeProviderCandidate:
    id: str
    name: str
    kind: str
    source_url: str
    base_url: str | None
    env_key: str | None
    requires_key: bool
    notes: str


CANDIDATES: tuple[FreeProviderCandidate, ...] = (
    FreeProviderCandidate(
        "freellmapi",
        "FreeLLMAPI",
        "aggregator",
        "https://github.com/tashfeenahmed/freellmapi",
        "http://localhost:8000/v1",
        "FREELLMAPI_API_KEY",
        True,
        "OpenAI-compatible proxy; aggregates free-tier providers and supports failover.",
    ),
    FreeProviderCandidate(
        "groq-free",
        "Groq",
        "provider",
        "https://console.groq.com",
        "https://api.groq.com/openai/v1",
        "GROQ_API_KEY",
        True,
        "Free tier; limits change and must be checked before use.",
    ),
    FreeProviderCandidate(
        "cerebras-free",
        "Cerebras",
        "provider",
        "https://cloud.cerebras.ai",
        "https://api.cerebras.ai/v1",
        "CEREBRAS_API_KEY",
        True,
        "Free tier; limits change and must be checked before use.",
    ),
    FreeProviderCandidate(
        "gemini-free",
        "Google Gemini",
        "provider",
        "https://ai.google.dev",
        "https://generativelanguage.googleapis.com/v1beta/openai/",
        "GEMINI_API_KEY",
        True,
        "Free-tier models vary; verify current quota in the provider account.",
    ),
    FreeProviderCandidate(
        "openrouter-free",
        "OpenRouter free models",
        "provider",
        "https://openrouter.ai",
        "https://openrouter.ai/api/v1",
        "OPENROUTER_API_KEY",
        True,
        "Use only models explicitly marked free; limits can change.",
    ),
    FreeProviderCandidate(
        "github-models",
        "GitHub Models",
        "provider",
        "https://github.com/marketplace/models",
        "https://models.inference.ai.azure.com",
        "GITHUB_TOKEN",
        True,
        "Availability and limits depend on the authenticated GitHub account.",
    ),
)


def candidates() -> list[dict]:
    return [c.__dict__.copy() for c in CANDIDATES]


def configured() -> list[dict]:
    return [
        c.__dict__.copy()
        for c in CANDIDATES
        if c.env_key and os.getenv(c.env_key)
    ]


def discover(extra: Iterable[FreeProviderCandidate] = ()) -> list[dict]:
    """Return public candidates plus configured state; no secret values are exposed."""
    rows = list(CANDIDATES) + list(extra)
    return [
        {
            **c.__dict__,
            "configured": bool(c.env_key and os.getenv(c.env_key)),
        }
        for c in rows
    ]


def health() -> dict:
    return {
        "status": "ok",
        "candidate_count": len(CANDIDATES),
        "configured_count": len(configured()),
        "secrets_exposed": False,
    }
