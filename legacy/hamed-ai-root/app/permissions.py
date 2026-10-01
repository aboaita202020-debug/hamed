"""Compatibility facade for the canonical server-side authority policy.

The implementation lives in ``app.agents.permissions``. Keeping this module
preserves older imports while ensuring every caller uses the same policy.
"""
from .agents.permissions import ApprovalRequest, Risk, can_execute


class PermissionLayer:
    """Small repository-compatible facade used by the orchestrator/tool layer."""

    def __init__(self, repo=None):
        self.repo = repo

    def can_execute(self, action: str, *, approved: bool = False,
                    value: float | None = None, risk: Risk = Risk.LOW) -> bool:
        return can_execute(action, approved=approved, value=value, risk=risk)


__all__ = ["ApprovalRequest", "Risk", "can_execute", "PermissionLayer"]
