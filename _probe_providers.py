"""One-shot probe of configured AI providers. Prints only status, never keys."""
from __future__ import annotations

import os
import sys
import time
import traceback

from app.agents.provider import MultiBrainProvider


def main() -> int:
    print("== configured env keys ==")
    for k in (
        "GEMINI_API_KEY", "KIMI_API_KEY", "MISTRAL_API_KEY", "QWEN_API_KEY",
        "XAI_API_KEY", "GROK_API_KEY", "LLAMA_API_KEY", "GROQ_API_KEY",
        "OPENROUTER_API_KEY", "DEEPSEEK_API_KEY", "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY", "TELEGRAM_BOT_TOKEN",
    ):
        print(f"  {k}: {'SET' if os.getenv(k, '').strip() else 'MISSING'}")

    try:
        provider = MultiBrainProvider()
    except Exception as exc:
        print("MultiBrainProvider init FAILED:", type(exc).__name__, exc)
        return 1

    print("== available brains ==", list(provider.available_brains()))

    print("== live chat probe ==")
    t0 = time.time()
    try:
        reply = provider.generate_response(
            [{"role": "user", "content": "Reply with exactly the two characters: OK"}],
            system="Reply with only the word OK. No punctuation, no explanation.",
        )
        print(f"  OK in {time.time()-t0:.2f}s -> {reply[:120]!r}")
    except Exception as exc:
        print(f"  FAILED in {time.time()-t0:.2f}s -> {type(exc).__name__}: {exc}")
        traceback.print_exc()

    print("== live web_research probe ==")
    t0 = time.time()
    try:
        reply = provider.web_research(
            "What is the current population of Cairo, Egypt? Answer in one sentence.",
            system="Answer concisely with a single sentence.",
        )
        print(f"  OK in {time.time()-t0:.2f}s -> {reply[:200]!r}")
    except Exception as exc:
        print(f"  FAILED in {time.time()-t0:.2f}s -> {type(exc).__name__}: {exc}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
