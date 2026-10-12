"""Brave Search API provider for WebSearchTool.

Requires BRAVE_API_KEY env var. Free tier available.
Spec-compliant: never fabricates; returns empty on error.
"""
from __future__ import annotations

import os
import time
from typing import List

import requests

from .base_tool import BaseTool, ToolResult, ToolSchema


class BraveSearchProvider:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("BRAVE_API_KEY", "").strip()
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key,
        })

    def search(self, query: str, max_results: int = 5) -> List[dict]:
        if not self.api_key:
            return []
        if not query or not query.strip():
            return []
        try:
            params = {
                "q": query,
                "count": max_results,
                "search_lang": "en",
                "country": "EG",
            }
            r = self.session.get("https://api.search.brave.com/res/v1/web/search", params=params, timeout=15)
            if r.status_code != 200:
                return []
            data = r.json()
            results = []
            for item in data.get("web", {}).get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", ""),
                    "source": "brave",
                    "confidence": 0.7,
                })
            return results
        except Exception:
            return []


class WebSearchToolWithBrave(BaseTool):
    schema = ToolSchema(
        name="web_search",
        description="Search the web for business facts using Brave Search API.",
        parameters={"query": "search text", "max_results": "int, default 5"},
        sensitive=False,
    )

    def __init__(self, provider=None):
        self.provider = provider or BraveSearchProvider()

    def run(self, query: str, max_results: int = 5) -> ToolResult:
        if not query or not query.strip():
            return ToolResult(success=False, error="empty query")
        try:
            raw = self.provider.search(query, max_results)
            if not raw:
                return ToolResult(success=False, error="no_results_found_or_no_key")
            data = []
            for r in raw:
                data.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("snippet", ""),
                    "source": r.get("source", "brave"),
                    "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "confidence": float(r.get("confidence", 0.5)),
                })
            return ToolResult(success=True, data=data)
        except Exception as exc:
            return ToolResult(success=False, error=f"provider_error: {exc}")
