"""Commercial web-research tool boundary.

Actual search is performed by the configured OpenAI web-search tool. This module
keeps a small, testable boundary for future non-OpenAI search providers.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class SearchRequest:
    query: str
    purpose: str = "commercial_research"


def validate_request(request: SearchRequest) -> SearchRequest:
    query = request.query.strip()
    if not query:
        raise ValueError("Search query cannot be empty")
    return SearchRequest(query=query, purpose=request.purpose)
