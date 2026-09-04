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
    # Prevent the repository's local .env from satisfying missing-secret tests.
    # Production startup still loads .env normally; this subprocess intentionally
    # validates the environment contract in isolation.
    clean["PYTHON_DOTENV_DISABLED"] = "1"
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


def _clear_brain_env(monkeypatch: pytest.MonkeyPatch):
    for key in (
        "OPENAI_API_KEY", "DEEPSEEK_API_KEY", "KIMI_API_KEY", "GEMINI_API_KEY",
        "MISTRAL_API_KEY", "QWEN_API_KEY", "XAI_API_KEY", "GROK_API_KEY",
        "LLAMA_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY",
    ):
        monkeypatch.delenv(key, raising=False)


def test_multibrain_loads_only_configured_fake_providers(monkeypatch: pytest.MonkeyPatch):
    _clear_brain_env(monkeypatch)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-placeholder")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "fake-deepseek")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-anthropic")

    provider = MultiBrainProvider()
    assert set(provider.available_brains()) == {"openai", "deepseek", "claude"}


def test_multibrain_loads_all_ten_brains_with_fake_credentials(monkeypatch: pytest.MonkeyPatch):
    _clear_brain_env(monkeypatch)
    fake_keys = {
        "OPENAI_API_KEY": "fake-openai",
        "ANTHROPIC_API_KEY": "fake-anthropic",
        "DEEPSEEK_API_KEY": "fake-deepseek",
        "KIMI_API_KEY": "fake-kimi",
        "GEMINI_API_KEY": "fake-gemini",
        "MISTRAL_API_KEY": "fake-mistral",
        "QWEN_API_KEY": "fake-qwen",
        "XAI_API_KEY": "fake-xai",
        "LLAMA_API_KEY": "fake-llama",
        "OPENROUTER_API_KEY": "fake-openrouter",
    }
    for key, value in fake_keys.items():
        monkeypatch.setenv(key, value)

    provider = MultiBrainProvider()
    assert set(provider.available_brains()) == {
        "openai", "claude", "deepseek", "kimi", "gemini",
        "mistral", "qwen", "grok", "llama", "openrouter",
    }


def test_grok_legacy_key_remains_compatible(monkeypatch: pytest.MonkeyPatch):
    _clear_brain_env(monkeypatch)
    monkeypatch.setenv("OPENAI_API_KEY", "fake-openai")
    monkeypatch.setenv("GROK_API_KEY", "fake-grok")
    provider = MultiBrainProvider()
    assert "grok" in provider.available_brains()


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
