"""Typed registry for narrowly scoped Hamed tools.

The model can select registered tools, but it cannot execute arbitrary shell,
SQL, HTTP, or filesystem operations through this registry.
"""
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    handler: Callable[..., Any]
    required_permission: str
    read_only: bool = True
    reversible: bool = True
    risk_level: str = "low"


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        if spec.name in self._tools:
            raise ValueError(f"Tool already registered: {spec.name}")
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(f"Unknown Hamed tool: {name}") from exc

    def list(self) -> tuple[ToolSpec, ...]:
        return tuple(self._tools.values())
