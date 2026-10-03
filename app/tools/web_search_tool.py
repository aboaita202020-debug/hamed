"""
WebSearchTool — spec section 17 (Web & Social Intelligence).

IMPORTANT (spec section 28: "لا يخترع بيانات أو أسعارًا أو شركات"):
This tool NEVER fabricates results. By default (no `provider` wired
in) it returns success=False with a clear "NO_PROVIDER_CONFIGURED"
error instead of inventing fake companies or prices — an Agent must
treat that as "insufficient information", not as data.

To go live, inject a `provider` callable that performs the real HTTP
call (e.g. to Bing/SerpAPI/Google CSE) via `requests`. Keeping that
behind a callable means Core has zero hard dependency on any single
search vendor (spec section 30: "لا تعتمد على خدمة مدفوعة واحدة").
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable, Optional

from .base_tool import BaseTool, ToolResult, ToolSchema

SearchProvider = Callable[[str, int], list[dict]]


class WebSearchTool(BaseTool):
    schema = ToolSchema(
        name="web_search",
        description="Search the web for a business fact (company, product, supplier, price).",
        parameters={"query": "search text", "max_results": "int, default 5"},
        sensitive=False,
    )

    def __init__(self, provider: Optional[SearchProvider] = None):
        self.provider = provider

    def run(self, query: str, max_results: int = 5) -> ToolResult:
        if not query or not query.strip():
            return ToolResult(success=False, error="empty query")

        if self.provider is None:
            return ToolResult(
                success=False,
                error="NO_PROVIDER_CONFIGURED: wire a real search provider before "
                      "relying on this tool for facts (see web_search_tool.py docstring).",
            )

        try:
            raw_results = self.provider(query, max_results)
        except Exception as exc:
            return ToolResult(success=False, error=f"provider_error: {exc}")

        results = [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("snippet", ""),
                "source": r.get("source", "web"),
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "confidence": r.get("confidence", 0.5),
            }
            for r in raw_results
        ]
        return ToolResult(success=True, data=results)
