from app.agents.provider import MultiBrainProvider


def test_ollama_is_available_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("HAMED_OLLAMA_ENABLED", "1")
    router = MultiBrainProvider()
    assert "ollama" in router.available_brains()


def test_claude_is_optional(monkeypatch):
    monkeypatch.setenv("HAMED_OLLAMA_ENABLED", "1")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    router = MultiBrainProvider()
    assert "claude" not in router.available_brains()
    assert "ollama" in router.available_brains()
