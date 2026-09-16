"""Multi-brain AI provider layer with free-first routing and broad public-web learning."""
from __future__ import annotations

import os
import re
import xml.etree.ElementTree as ET
from html import unescape
from typing import Protocol
from urllib.parse import quote_plus, urlparse

import requests


class AIProvider(Protocol):
    def generate_response(self, messages, *, system: str = "") -> str: ...
    def web_research(self, query: str, *, system: str = "") -> str: ...


def _clean_html(text: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>|<style.*?>.*?</style>|<noscript.*?>.*?</noscript>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _host(url: str) -> str:
    try:
        return urlparse(url).netloc.lower().removeprefix("www.")
    except Exception:
        return "web"


def public_web_research(query: str, max_results: int = 12) -> str:
    """Collect evidence from multiple free public web sources before an AI summarizes it.

    This intentionally uses several independent source families instead of pretending that an
    LLM itself is a web browser: general search, news RSS, Wikipedia, Crossref, Open Library,
    Internet Archive, and YouTube-focused search results. Network failures are isolated per source.
    """
    headers = {"User-Agent": "HamedAI/1.0 (autonomous-learning; public-web-research)"}
    timeout = int(os.getenv("HAMED_WEB_TIMEOUT", "12"))
    query = query.strip()
    if not query:
        return "NO_QUERY"

    results: list[dict] = []
    seen: set[str] = set()

    def add(title: str, url: str, snippet: str, source: str) -> None:
        url = (url or "").strip()
        snippet = re.sub(r"\s+", " ", unescape(snippet or "")).strip()
        if not url or url in seen:
            return
        seen.add(url)
        results.append({"title": title.strip() or "Untitled", "url": url, "snippet": snippet[:1800], "source": source})

    # 1) General web search through DuckDuckGo's public HTML endpoint.
    ddg_queries = [
        query,
        query + " research report statistics",
        query + " practical guide case study",
        query + " site:youtube.com interview course lecture",
    ]
    for q in ddg_queries:
        try:
            html = requests.get("https://html.duckduckgo.com/html/?q=" + quote_plus(q), headers=headers, timeout=timeout).text
            for block in re.findall(r'(?is)<div class="result__body".*?</div>\s*</div>', html):
                link = re.search(r'(?is)<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', block)
                if not link:
                    continue
                url = unescape(link.group(1))
                title = _clean_html(link.group(2))
                snippet_match = re.search(r'(?is)result__snippet[^>]*>(.*?)</a?>', block)
                snippet = _clean_html(snippet_match.group(1)) if snippet_match else ""
                add(title, url, snippet, "duckduckgo")
                if len(results) >= max_results:
                    break
        except Exception:
            continue
        if len(results) >= max_results:
            break

    # 2) Google News RSS: current public news and market signals without an API key.
    try:
        rss = requests.get(
            "https://news.google.com/rss/search?q=" + quote_plus(query) + "&hl=en-US&gl=US&ceid=US:en",
            headers=headers,
            timeout=timeout,
        ).text
        root = ET.fromstring(rss)
        for item in root.findall(".//item")[:8]:
            title = item.findtext("title") or ""
            url = item.findtext("link") or ""
            desc = _clean_html(item.findtext("description") or "")
            add(title, url, desc, "google_news_rss")
    except Exception:
        pass

    # 3) Wikipedia / Wikimedia public knowledge.
    try:
        data = requests.get(
            "https://en.wikipedia.org/api/rest_v1/page/summary/" + quote_plus(query.replace(" ", "_")),
            headers=headers,
            timeout=timeout,
        ).json()
        if data.get("content_urls", {}).get("desktop", {}).get("page"):
            add(data.get("title", query), data["content_urls"]["desktop"]["page"], data.get("extract", ""), "wikipedia")
    except Exception:
        pass

    # 4) Academic metadata through Crossref.
    try:
        data = requests.get(
            "https://api.crossref.org/works?query.bibliographic=" + quote_plus(query) + "&rows=6",
            headers=headers,
            timeout=timeout,
        ).json()
        for item in data.get("message", {}).get("items", []):
            title = " ".join(item.get("title") or [])
            url = item.get("URL") or ""
            abstract = _clean_html(item.get("abstract") or "")
            if title and url:
                add(title, url, abstract or ("Authors: " + ", ".join(a.get("family", "") for a in item.get("author", []))), "crossref")
    except Exception:
        pass

    # 5) Books and educational material through Open Library.
    try:
        data = requests.get(
            "https://openlibrary.org/search.json?q=" + quote_plus(query) + "&limit=6",
            headers=headers,
            timeout=timeout,
        ).json()
        for doc in data.get("docs", [])[:6]:
            key = doc.get("key", "")
            title = doc.get("title", "")
            if key and title:
                add(title, "https://openlibrary.org" + key, "Authors: " + ", ".join(doc.get("author_name", [])[:4]), "open_library")
    except Exception:
        pass

    # 6) Public archive / documents.
    try:
        data = requests.get(
            "https://archive.org/advancedsearch.php?q=" + quote_plus(query) + "&fl[]=identifier,title,description&rows=6&page=1&output=json",
            headers=headers,
            timeout=timeout,
        ).json()
        for doc in data.get("response", {}).get("docs", [])[:6]:
            ident = doc.get("identifier", "")
            if ident:
                add(doc.get("title", ident), "https://archive.org/details/" + ident, _clean_html(str(doc.get("description", ""))), "internet_archive")
    except Exception:
        pass

    # Fetch a small amount of primary page text from the best general results.
    fetched = 0
    for item in list(results):
        if fetched >= 5:
            break
        if item["source"] not in {"duckduckgo", "google_news_rss"}:
            continue
        try:
            page = requests.get(item["url"], headers=headers, timeout=timeout, allow_redirects=True)
            content_type = page.headers.get("content-type", "")
            if page.ok and "text/html" in content_type:
                text = _clean_html(page.text)
                if len(text) > 300:
                    item["snippet"] = (item["snippet"] + " | PAGE TEXT: " + text[:4500])[:6000]
                    fetched += 1
        except Exception:
            continue

    if not results:
        raise RuntimeError("PUBLIC_WEB_RESEARCH_RETURNED_NO_SOURCES")

    lines = [
        "PUBLIC WEB EVIDENCE — collected before AI synthesis",
        f"Query: {query}",
        f"Source records: {len(results)}",
        "Source families: general web search, news RSS, Wikipedia, academic metadata, books, public archive; YouTube-focused results when indexed by search.",
        "",
    ]
    for i, item in enumerate(results[:max_results], 1):
        lines.append(f"[{i}] {item['title']} | source={item['source']} | host={_host(item['url'])}")
        lines.append(f"URL: {item['url']}")
        if item["snippet"]:
            lines.append(f"Evidence: {item['snippet']}")
        lines.append("")
    return "\n".join(lines)


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
        evidence = public_web_research(query)
        return self.generate_response([{"role": "user", "content": evidence}], system=system or "Synthesize only supported evidence; never invent sources.")


class OpenAICompatibleProvider:
    def __init__(self, name, api_key, base_url, model, timeout=60):
        self.name, self.api_key, self.base_url, self.model, self.timeout = name, api_key, base_url.rstrip("/"), model, timeout

    def generate_response(self, messages, *, system=""):
        payload = list(messages)
        if system:
            payload.insert(0, {"role": "system", "content": system})
        r = requests.post(self.base_url + "/chat/completions", headers={"Authorization": "Bearer " + self.api_key, "Content-Type": "application/json"}, json={"model": self.model, "messages": payload}, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        return str(data["choices"][0]["message"].get("content") or "").strip()

    def web_research(self, query, *, system=""):
        evidence = public_web_research(query)
        return self.generate_response([{"role": "user", "content": evidence}], system=system or "Synthesize only supported evidence; never invent sources.")


class OllamaProvider:
    """Local, keyless brain. Requires an Ollama server on the user's machine."""

    def __init__(self, model: str = "llama3.2:3b", base_url: str = "http://127.0.0.1:11434", timeout: int = 120) -> None:
        self.model, self.base_url, self.timeout = model, base_url.rstrip("/"), timeout

    def generate_response(self, messages, *, system=""):
        prompt_messages = list(messages)
        if system:
            prompt_messages.insert(0, {"role": "system", "content": system})
        r = requests.post(self.base_url + "/api/chat", json={"model": self.model, "messages": prompt_messages, "stream": False}, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        return str(data.get("message", {}).get("content") or "").strip()

    def web_research(self, query, *, system=""):
        evidence = public_web_research(query)
        return self.generate_response([{"role": "user", "content": evidence}], system=system or "Synthesize only supported evidence; cite the supplied URLs and distinguish evidence from inference.")


class GeminiProvider:
    """Native Gemini REST provider; avoids OpenAI-compatibility 404s."""
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash-lite", timeout: int = 60) -> None:
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required")
        self.api_key, self.model, self.timeout = api_key, model, timeout
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def generate_response(self, messages, *, system=""):
        contents = []
        for message in messages:
            role, text = message.get("role", "user"), str(message.get("content") or "")
            if text:
                contents.append({"role": "model" if role == "assistant" else "user", "parts": [{"text": text}]})
        if not contents:
            contents = [{"role": "user", "parts": [{"text": "Hello"}]}]
        payload = {"contents": contents}
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        r = requests.post(self.base_url + "/" + self.model + ":generateContent", params={"key": self.api_key}, headers={"Content-Type": "application/json"}, json=payload, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        return "".join(str(part["text"]) for candidate in data.get("candidates", []) for part in candidate.get("content", {}).get("parts", []) if part.get("text")).strip()

    def web_research(self, query, *, system=""):
        evidence = public_web_research(query)
        return self.generate_response([{"role": "user", "content": evidence}], system=system or "Synthesize only supported evidence; cite supplied URLs.")


class AnthropicProvider:
    def __init__(self, api_key, model, workspace_id=""):
        from anthropic import Anthropic
        kwargs = {"api_key": api_key}
        if workspace_id:
            kwargs["default_headers"] = {"anthropic-workspace-id": workspace_id}
        self.client, self.model = Anthropic(**kwargs), model

    def generate_response(self, messages, *, system=""):
        response = self.client.messages.create(model=self.model, max_tokens=4096, system=system or "You are a helpful AI assistant.", messages=[m for m in messages if m["role"] != "system"])
        return "".join(getattr(block, "text", "") for block in response.content).strip()

    def web_research(self, query, *, system=""):
        evidence = public_web_research(query)
        return self.generate_response([{"role": "user", "content": evidence}], system=system or "Synthesize only supported evidence; cite supplied URLs.")


class BrainSelector:
    """Deterministic free-first capability/availability ordering."""
    def rank(self, task, available, *, complexity="medium", cost_sensitive=False):
        t, available = task.lower(), list(available)
        if any(x in t for x in ("code", "python", "javascript", "برمج", "كود", "docker")):
            preferred = ["ollama", "gemini", "kimi", "deepseek", "claude", "openai"]
        elif any(x in t for x in ("research", "بحث", "مصادر", "سوق")):
            preferred = ["ollama", "gemini", "kimi", "claude", "openai", "deepseek"]
        elif any(x in t for x in ("sales", "بيع", "تسويق", "marketing", "عميل")):
            preferred = ["ollama", "gemini", "kimi", "claude", "openai", "deepseek"]
        else:
            preferred = ["ollama", "gemini", "kimi", "claude", "openai", "deepseek"]
        if cost_sensitive or os.getenv("HAMED_FREE_FIRST", "1").lower() not in {"0", "false", "no"}:
            preferred = ["ollama", "gemini", "kimi"] + preferred
        return list(dict.fromkeys(x for x in preferred + available if x in available))


class MultiBrainProvider:
    """Multi-brain router. Claude is optional; Hamed can run without paid AI."""
    def __init__(self):
        self.providers = {}
        self._load()
        if not self.providers:
            raise RuntimeError("No AI brain is available. Install/start Ollama or configure a supported provider API key.")

    def _load(self):
        if os.getenv("HAMED_OLLAMA_ENABLED", "1").lower() not in {"0", "false", "no"}:
            self.providers["ollama"] = OllamaProvider(os.getenv("OLLAMA_MODEL", "llama3.2:3b"), os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434"))
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
        errors = []
        for name in self._order(query):
            try:
                result = self.providers[name].web_research(query, system=system)
                if result:
                    return result
            except Exception as exc:
                errors.append(name + ":" + type(exc).__name__)
        raise RuntimeError("All configured AI brains failed research: " + ", ".join(errors))

    def available_brains(self):
        return tuple(self.providers)
