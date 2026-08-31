"""Pluggable source registry for Hamed continuous learning.

Connectors are intentionally interfaces: concrete providers can be enabled in
configuration without embedding credentials or pretending unavailable sources
were fetched.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Source:
    name: str
    source_type: str
    uri: str
    title: str = ""


class SourceConnector(Protocol):
    name: str
    def search(self, query: str, limit: int = 10) -> list[Source]: ...


class SourceRegistry:
    def __init__(self) -> None:
        self._connectors: dict[str, SourceConnector] = {}

    def register(self, connector: SourceConnector) -> None:
        self._connectors[connector.name] = connector

    def available(self) -> list[str]:
        return sorted(self._connectors)

    def search_all(self, query: str, limit_per_source: int = 5) -> list[Source]:
        results: list[Source] = []
        for connector in self._connectors.values():
            try:
                results.extend(connector.search(query, limit_per_source))
            except Exception:
                # One unavailable source must not stop the learning cycle.
                continue
        return results
