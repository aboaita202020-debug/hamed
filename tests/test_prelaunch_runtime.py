from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from app.agents.provider import MultiBrainProvider

ROOT = Path(__file__).resolve().parents[1]


def run_bot(env: dict[str, str]):
    clean = os.environ.copy()
    for key in (
        "TELEGRAM_BOT_TOKEN",
        "OPENAI_API_KEY",
        "HAMED_TELEGRAM_POLLING",
        "DATABASE_URL",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "PAYMOB_API_KEY",
    ):
        clean.pop(key, None)
    clean.update(env)
    return subprocess.run(
        [sys.executable, "bot.py"],
        cwd=ROOT,
        env=clean,
        capture_output=True,
        text=True,
        timeout=10,
    )


def test_startup_fails_cleanly_when_telegram_token_is_missing():
    result = run_bot({"OPENAI_API_KEY": "sk-test-placeholder"})
    assert result.returncode != 0
    assert "TELEGRAM_BOT_TOKEN" in result.stderr
    assert "sk-test-placeholder" not in result.stderr


def test_startup_fails_cleanly_when_openai_key_is_missing():
    result = run_bot({"TELEGRAM_BOT_TOKEN": "12345:TEST_TOKEN_PLACEHOLDER"})
    assert result.returncode != 0
    assert "OPENAI_API_KEY" in result.stderr
    assert "12345:TEST_TOKEN_PLACEHOLDER" not in result.stderr


def test_multibrain_loads_only_configured_fake_providers(monkeypatch: pytest.MonkeyPatch):
    for key in (
        "OPENAI_API_KEY",
        "DEEPSEEK_API_KEY",
        "KIMI_API_KEY",
        "GEMINI_API_KEY",
        "MISTRAL_API_KEY",
        "QWEN_API_KEY",
        "GROK_API_KEY",
        "LLAMA_API_KEY",
        "OPENROUTER_API_KEY",
        "ANTHROPIC_API_KEY",
    ):
        monkeypatch.delenv(key, raising=False)

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-placeholder")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "fake-deepseek")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-anthropic")

    provider = MultiBrainProvider()
    assert set(provider.available_brains()) == {"openai", "deepseek", "claude"}


def test_multibrain_fallback_uses_next_provider(monkeypatch: pytest.MonkeyPatch):
    provider = MultiBrainProvider.__new__(MultiBrainProvider)

    class Broken:
        def generate_response(self, messages, *, system=""):
            raise RuntimeError("simulated failure")

    class Working:
        def generate_response(self, messages, *, system=""):
            return "mock response"

    provider.providers = {"openai": Broken(), "deepseek": Working()}
    assert provider.generate_response([{"role": "user", "content": "hello"}]) == "mock response"
