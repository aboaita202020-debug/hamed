"""
Every Tool has a clear schema (spec section 30: "كل Tool لها schema واضح")
and declares whether calling it is "sensitive" (must go through the
Permission Layer) or safe to auto-run.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolResult:
    success: bool
    data: Any = None
    error: str = ""


@dataclass
class ToolSchema:
    name: str
    description: str
    parameters: dict = field(default_factory=dict)  # {param_name: description}
    sensitive: bool = False  # True => must pass through PermissionLayer


class BaseTool:
    """Subclass this for every tool. `schema` must be set by subclasses."""

    schema: ToolSchema

    def run(self, **kwargs) -> ToolResult:  # pragma: no cover - interface
        raise NotImplementedError
