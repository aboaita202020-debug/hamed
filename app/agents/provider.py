"""Multi-brain AI provider layer with free-first routing and safe fallback."""
from __future__ import annotations

import os
from typing import Protocol

import requests


class AIProvider(Protocol):
    def generate_response(self, messages, *, system: str = "") -> str: ...
    def web_research(self, query: str, *, system: str = "") -> str: ...


class OpenAIProvider:
    def __init__(self, api_key: str, model: str = "gpt-5") -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")
        from openai import OpenAI
        self.client, self.model = OpenAI(api_key=api_key), model

    def generate_response(self, messages, *, system=""):
        payload = list(messages)
        if system:
            payload.insert(0, {"role": "system", "content": system})
        response = self.client.chat.completions.create(model=self.model, messages=payload)
        return (response.choices[0].message.content or "").strip()

    def web_research(self, query, *, system=""):
        return self.generate_response(
            [{"role": "user", "content": query}],
            system=system or "Use supported evidence; never invent sources.",
        )


class OpenAICompatibleProvider:
    def __init__(self, name, api_key, base_url, model, timeout=60):
        self.name = name
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate_response(self, messages, *, system=""):
        payload = list(messages)
        if system:
            payload.insert(0, {"role": "system", "content": system})
        r = requests.post(
            self.base_url + "/chat/completions",
            headers={
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "application/json",
            },
            json={"model": self.model, "messages": payload},
            timeout=self.timeout,
        )
        r.raise_for_status()
        data = r.json()
        return str(data["choices"][0]["message"].get("content") or "").strip()

    def web_research(self, query, *, system=""):
        return self.generate_response([{"role": "user", "content": query}], system=system)


class OllamaProvider:
    """Local, keyless brain. Requires an Ollama server on the user's machine."""

    def __init__(self, model: str = "llama3.2:3b", base_url: str = "http://127.0.0.1:11434", timeout: int = 120) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate_response(self, messages, *, system=""):
        prompt_messages = list(messages)
        if system:
            prompt_messages.insert(0, {"role": "system", "content": system})
        r = requests.post(
            self.base_url + "/api/chat",
            json={"model": self.model, "messages": prompt_messages, "stream": False},
            timeout=self.timeout,
        )
        r.raise_for_status()
        data = r.json()
        return str(data.get("message", {}).get("content") or "").strip()

    def web_research(self, query, *, system=""):
        return self.generate_response([{"role": "user", "content": query}], system=system)


class GeminiProvider:
    """Native Gemini REST provider; avoids OpenAI-compatibility 404s."""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash-lite", timeout: int = 60) -> None:
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def generate_response(self, messages, *, system=""):
        contents = []
        for message in messages:
            role = message.get("role", "user")
            text = str(message.get("content") or "")
            if not text:
                continue
            contents.append({"role": "model" if role == "assistant" else "user", "parts": [{"text": text}]})
        if not contents:
            contents = [{"role": "user", "parts": [{"text": "Hello"}]}]
        payload = {"contents": contents}
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        url = self.base_url + "/" + self.model + ":generateContent"
        r = requests.post(url, params={"key": self.api_key}, headers={"Content-Type": "application/json"}, json=payload, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        parts = []
        for candidate in data.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if part.get("text"):
                    parts.append(str(part["text"]))
        return "".join(parts).strip()

    def web_research(self, query, *, system=""):
        return self.generate_response([{"role": "user", "content": query}], system=system)


class AnthropicProvider:
    def __init__(self, api_key, model, workspace_id=""):
        from anthropic import Anthropic
        kwargs = {"api_key": api_key}
        if workspace_id:
            kwargs["default_headers"] = {"anthropic-workspace-id": workspace_id}
        self.client, self.model = Anthropic(**kwargs), model

    def generate_response(self, messages, *, system=""):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system or "You are a helpful AI assistant.",
            messages=[m for m in messages if m["role"] != "system"],
        )
        return "".join(getattr(block, "text", "") for block in response.content).strip()

    def web_research(self, query, *, system=""):
        return self.generate_response([{"role": "user", "content": query}], system=system)


class BrainSelector:
    """Deterministic free-first capability/availability ordering."""

    def rank(self, task, available, *, complexity="medium", cost_sensitive=False):
        t = task.lower()
        available = list(available)
        if any(x in t for x in ("code", "python", "javascript", "برمج", "كود", "docker")):
            preferred = ["ollama", "gemini", "kimi", "deepseek", "claude", "openai"]
        elif any(x in t for x in ("research", "بحث", "مصادر", "سوق")):
            preferred = ["gemini", "ollama", "kimi", "claude", "openai", "deepseek"]
        elif any(x in t for x in ("sales", "بيع", "تسويق", "marketing", "عميل")):
            preferred = ["gemini", "ollama", "kimi", "claude", "openai", "deepseek"]
        else:
            preferred = ["ollama", "gemini", "kimi", "claude", "openai", "deepseek"]
        if cost_sensitive or os.getenv("HAMED_FREE_FIRST", "1").lower() not in {"0", "false", "no"}:
            preferred = ["ollama", "gemini", "kimi"] + preferred
        return list(dict.fromkeys(x for x in preferred + available if x in available))


class MultiBrainProvider:
    """Multi-brain router. Claude is optional; Hamed can run without any paid subscription."""

    def __init__(self):
        self.providers = {}
        self._load()
        if not self.providers:
            raise RuntimeError(
                "No AI brain is available. Install/start Ollama for keyless local AI "
                "or configure at least one supported provider API key."
            )

    def _load(self):
        # Local Ollama is enabled by default and requires no subscription or API key.
        if os.getenv("HAMED_OLLAMA_ENABLED", "1").lower() not in {"0", "false", "no"}:
            self.providers["ollama"] = OllamaProvider(
                os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
                os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
            )

        key = os.getenv("GEMINI_API_KEY", "").strip()
        if key:
            self.providers["gemini"] = GeminiProvider(key, os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"))

        key = os.getenv("KIMI_API_KEY", "").strip()
        if key:
            self.providers["kimi"] = OpenAICompatibleProvider("kimi", key, os.getenv("KIMI_API_BASE_URL", "https://api.moonshot.ai/v1"), os.getenv("KIMI_MODEL", "kimi-k2-0905-preview"))

        compatible = [
            ("mistral", "MISTRAL_API_KEY", "https://api.mistral.ai/v1", "MISTRAL_MODEL", "mistral-small-latest"),
            ("qwen", "QWEN_API_KEY", "https://dashscope.aliyuncs.com/compatible-mode/v1", "QWEN_MODEL", "qwen-plus"),
            ("grok", "XAI_API_KEY", "https://api.x.ai/v1", "XAI_MODEL", "grok-3-mini"),
            ("llama", "LLAMA_API_KEY", "https://api.groq.com/openai/v1", "LLAMA_MODEL", "llama-4-scout-17b-16e-instruct"),
            ("openrouter", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1", "OPENROUTER_MODEL", "openai/gpt-4o-mini"),
            ("deepseek", "DEEPSEEK_API_KEY", "https://api.deepseek.com", "DEEPSEEK_MODEL", "deepseek-chat"),
        ]
        for name, env, url, model_env, default in compatible:
            value = os.getenv(env, "").strip()
            if name == "grok" and not value:
                value = os.getenv("GROK_API_KEY", "").strip()
                model_env = "GROK_MODEL" if value else model_env
            if name == "llama" and not value:
                value = os.getenv("GROQ_API_KEY", "").strip()
            if value:
                self.providers[name] = OpenAICompatibleProvider(name, value, os.getenv(env + "_BASE_URL", url), os.getenv(model_env, default))

        key = os.getenv("OPENAI_API_KEY", "").strip()
        if key:
            self.providers["openai"] = OpenAIProvider(key, os.getenv("OPENAI_MODEL", "gpt-5"))

        # Claude is optional. It is never required for startup or normal operation.
        key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if key:
            self.providers["claude"] = AnthropicProvider(key, os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"), os.getenv("ANTHROPIC_WORKSPACE_ID", "").strip())

    def _order(self, task):
        return BrainSelector().rank(task, tuple(self.providers))

    def generate_response(self, messages, *, system=""):
        task = messages[-1].get("content", "") if messages else system
        errors = []
        for name in self._order(task):
            try:
                result = self.providers[name].generate_response(messages, system=system)
                if result:
                    return result
            except Exception as exc:
                errors.append(name + ":" + type(exc).__name__)
        raise RuntimeError("All configured AI brains failed: " + ", ".join(errors))

    def web_research(self, query, *, system=""):
        for name in self._order(query):
            try:
                result = self.providers[name].web_research(query, system=system)
                if result:
                    return result
            except Exception:
                continue
        raise RuntimeError("All configured AI brains failed research")

    def available_brains(self):
        return tuple(self.providers)
