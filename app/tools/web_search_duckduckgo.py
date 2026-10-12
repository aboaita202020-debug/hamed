"""Free DuckDuckGo HTML search provider for WebSearchTool.

No API key required. Uses DuckDuckGo HTML results page and parses snippets.
Spec-compliant: never fabricates results; returns empty list on failure.
"""
from __future__ import annotations

import re
import time
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from .base_tool import BaseTool, ToolResult, ToolSchema


class DuckDuckGoSearchProvider:
    """Simple DuckDuckGo HTML search provider with bot challenge detection."""

    def __init__(self, user_agent: str = "Mozilla/5.0"):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })

    def search(self, query: str, max_results: int = 5) -> List[dict]:
        if not query or not query.strip():
            return []
        try:
            params = {"q": query, "kl": "us-en"}
            r = self.session.get("https://duckduckgo.com/html/", params=params, timeout=15)
            r.raise_for_status()
        except Exception:
            return []
        # Detect bot challenge
        if "anomaly-modal" in r.text or "Please complete the following challenge" in r.text:
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        for a in soup.select("a.result__a")[:max_results]:
            title = a.get_text(strip=True)
            url = a.get("href", "")
            # snippet
            snippet_el = a.find_parent("div", class_="result")
            snippet = ""
            if snippet_el:
                sn = snippet_el.select_one(".result__snippet")
                if sn:
                    snippet = sn.get_text(" ", strip=True)
            results.append({
                "title": title,
                "url": url,
                "snippet": snippet,
                "source": "duckduckgo",
                "confidence": 0.6,
            })
        # rate limit politeness
        time.sleep(0.5)
        return results


class WebSearchToolWithDuckDuckGo(BaseTool):
    """WebSearchTool wired to DuckDuckGo free provider."""

    schema = ToolSchema(
        name="web_search",
        description="Search the web for business facts using DuckDuckGo.",
        parameters={"query": "search text", "max_results": "int, default 5"},
        sensitive=False,
    )

    def __init__(self, provider=None):
        self.provider = provider or DuckDuckGoSearchProvider()

    def run(self, query: str, max_results: int = 5) -> ToolResult:
        if not query or not query.strip():
            return ToolResult(success=False, error="empty query")
        try:
            raw = self.provider.search(query, max_results)
            if not raw:
                return ToolResult(success=False, error="no_results_found")
            data = []
            for r in raw:
                data.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("snippet", ""),
                    "source": r.get("source", "duckduckgo"),
                    "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "confidence": float(r.get("confidence", 0.5)),
                })
            return ToolResult(success=True, data=data)
        except Exception as exc:
            return ToolResult(success=False, error=f"provider_error: {exc}")
