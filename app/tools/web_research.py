"""Safe web research adapter for commercial discovery.

The model requests a search; the application returns structured evidence. Search is read-only.
"""
from dataclasses import dataclass
from urllib.parse import quote
from urllib.request import Request, urlopen
import json


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    snippet: str


def build_search_url(query: str) -> str:
    return "https://www.google.com/search?q=" + quote(query)


def search(query: str, timeout: int = 10) -> list[SearchResult]:
    if not query.strip():
        return []
    # This adapter intentionally returns a safe placeholder until a configured
    # search provider is enabled; it never fabricates supplier/product results.
    return []
