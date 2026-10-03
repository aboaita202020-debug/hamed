"""
ToolRegistry: where Agents look up Tools by name and execute them.
Every sensitive Tool call is routed through the PermissionLayer first
(spec section 30: "كل Tool حساسة تمر عبر Permission Layer").
"""
from __future__ import annotations

from typing import Optional

from app.permissions import PermissionLayer, PermissionCheck, ApprovalRequired
from app.logging_config import get_logger
from .base_tool import BaseTool, ToolResult

logger = get_logger(__name__)


class ToolRegistry:
    def __init__(self, permission_layer: Optional[PermissionLayer] = None):
        self._tools: dict[str, BaseTool] = {}
        self.permissions = permission_layer

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.schema.name] = tool

    def get(self, name: str) -> BaseTool:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered.")
        return self._tools[name]

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

    def execute(
        self,
        actor: str,
        tool_name: str,
        reason: str = "",
        amount_egp: float = 0.0,
        is_contract: bool = False,
        **kwargs,
    ) -> ToolResult:
        tool = self.get(tool_name)

        if tool.schema.sensitive and self.permissions:
            check = PermissionCheck(
                action=tool_name,
                amount_egp=amount_egp,
                is_contract=is_contract,
            )
            try:
                self.permissions.authorize(actor, check, reason=reason, input_data=kwargs)
            except ApprovalRequired as exc:
                logger.info("Tool '%s' blocked pending approval: %s", tool_name, exc)
                return ToolResult(success=False, error=str(exc))

        try:
            return tool.run(**kwargs)
        except Exception as exc:  # tools must never crash the Orchestrator
            logger.exception("Tool '%s' raised an exception", tool_name)
            return ToolResult(success=False, error=str(exc))
