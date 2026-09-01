"""Multi-brain AI provider layer with optional providers and safe fallback."""
from __future__ import annotations

import os
from typing import Protocol

import requests


class AIProvider(Protocol):
    def generate_response(self, messages: list[dict[str, str]], *, system: str = "") -> str: ...
    def web_research(self, query: str, *, system: str = "") -> str: ...


class OpenAIProvider:
    def __init__(self, api_key: str, model: str = "gpt-5") -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_response(self, messages, *, system=""):
        payload = list(messages)
        if system:
            payload.insert(0, {"role": "system", "content": system})
        response = self.client.chat.completions.create(model=self.model, messages=payload)
        return (response.choices[0].message.content or "").strip()

    def web_research(self, query, *, system=""):
        return self.generate_response([{"role": "user", "content": query}], system=system or "Research using supported evidence. Do not invent facts or sources.")


class OpenAICompatibleProvider:
    """Adapter for OpenAI-compatible APIs."""
    def __init__(self, name, api_key, base_url, model, timeout=60):
        self.name, self.api_key, self.base_url, self.model, self.timeout = name, api_key, base_url.rstrip("/"), model, timeout

    def generate_response(self, messages, *, system=""):
        payload = list(messages)
        if system:
            payload.insert(0, {"role": "system", "content": system})
        r = requests.post(
            self.base_url + "/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"model": self.model, "messages": payload}, timeout=self.timeout,
        )
        r.raise_for_status()
        return str(r.json()["choices"][0]["message"].get("content") or "").strip()

    def web_research(self, query, *, system=""):
        return self.generate_response([{"role": "user", "content": query}], system=system)


class AnthropicProvider:
    def __init__(self, api_key, model):
        from anthropic import Anthropic
        self.client, self.model = Anthropic(api_key=api_key), model

    def generate_response(self, messages, *, system=""):
        response = self.client.messages.create(
            model=self.model, max_tokens=4096, system=system or "You are a helpful AI assistant.",
            messages=[m for m in messages if m["role"] != "system"],
        )
        return "".join(getattr(block, "text", "") for block in response.content).strip()

    def web_research(self, query, *, system=""):
        return self.generate_response([{"role": "user", "content": query}], system=system)


class MultiBrainProvider:
    """Ten-brain router with task-aware selection and automatic fallback."""
    def __init__(self):
        self.providers = {}
        self._load()
        if not self.providers:
            raise RuntimeError("At least one AI provider must be configured")

    def _load(self):
        key = os.getenv("OPENAI_API_KEY", "").strip()
        if key:
            self.providers["openai"] = OpenAIProvider(key, os.getenv("OPENAI_MODEL", "gpt-5"))
        compatible = [
            ("deepseek", "DEEPSEEK_API_KEY", "https://api.deepseek.com", "DEEPSEEK_MODEL", "deepseek-chat"),
            ("kimi", "KIMI_API_KEY", "https://api.moonshot.ai/v1", "KIMI_MODEL", "kimi-k2-0905-preview"),
            ("gemini", "GEMINI_API_KEY", "https://generativelanguage.googleapis.com/v1beta/openai", "GEMINI_MODEL", "gemini-2.5-flash"),
            ("mistral", "MISTRAL_API_KEY", "https://api.mistral.ai/v1", "MISTRAL_MODEL", "mistral-small-latest"),
            ("qwen", "QWEN_API_KEY", "https://dashscope.aliyuncs.com/compatible-mode/v1", "QWEN_MODEL", "qwen-plus"),
            ("grok", "XAI_API_KEY", "https://api.x.ai/v1", "XAI_MODEL", "grok-3-mini"),
            ("llama", "LLAMA_API_KEY", "https://api.groq.com/openai/v1", "LLAMA_MODEL", "llama-4-scout-17b-16e-instruct"),
            ("openrouter", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1", "OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        ]
        for name, env, url, model_env, default in compatible:
            value = os.getenv(env, "").strip()
            if name == "grok" and not value:
                value = os.getenv("GROK_API_KEY", "").strip()
                model_env = "GROK_MODEL" if value else model_env
            if value:
                base_url = os.getenv(env + "_BASE_URL", url)
                self.providers[name] = OpenAICompatibleProvider(name, value, base_url, os.getenv(model_env, default))
        key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if key:
            self.providers["claude"] = AnthropicProvider(key, os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"))

    def _order(self, task):
        t = task.lower()
        if any(x in t for x in ("code", "python", "javascript", "برمج", "كود", "docker", "github")):
            preferred = ["deepseek", "claude", "openai", "qwen", "llama"]
        elif any(x in t for x in ("ملف", "مستند", "document", "long", "تحليل")):
            preferred = ["kimi", "claude", "gemini", "openai", "llama"]
        elif any(x in t for x in ("بيع", "مبيعات", "sales", "عميل", "تسويق", "marketing")):
            preferred = ["claude", "openai", "gemini", "kimi", "qwen"]
        else:
            preferred = ["openai", "claude", "gemini", "deepseek", "kimi", "qwen", "mistral", "grok", "llama", "openrouter"]
        return list(dict.fromkeys(preferred + list(self.providers)))

    def generate_response(self, messages, *, system=""):
        task = messages[-1].get("content", "") if messages else system
        errors = []
        for name in self._order(task):
            provider = self.providers.get(name)
            if not provider:
                continue
            try:
                result = provider.generate_response(messages, system=system)
                if result:
                    return result
            except Exception as exc:
                errors.append(f"{name}:{type(exc).__name__}")
        raise RuntimeError("All configured AI brains failed: " + ", ".join(errors))

    def web_research(self, query, *, system=""):
        for name in self._order(query):
            provider = self.providers.get(name)
            if not provider:
                continue
            try:
                result = provider.web_research(query, system=system)
                if result:
                    return result
            except Exception:
                continue
        raise RuntimeError("All configured AI brains failed research")

    def available_brains(self):
        return tuple(self.providers)
