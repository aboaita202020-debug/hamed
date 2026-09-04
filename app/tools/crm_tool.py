"""CRMTool — thin Tool wrapper over Repository for Agent use (spec section 14)."""
from __future__ import annotations

from app.db.repository import Repository
from .base_tool import BaseTool, ToolResult, ToolSchema


class CRMTool(BaseTool):
    schema = ToolSchema(
        name="crm_upsert_lead",
        description="Create or update (dedup by contact) a lead in the CRM.",
        parameters={
            "name": "lead name",
            "contact": "unique contact identifier (phone/email/handle)",
            "source": "where the lead came from",
            "stage": "pipeline stage, defaults to NEW_LEAD",
        },
        sensitive=False,
    )

    def __init__(self, repository: Repository):
        self.repo = repository

    def run(self, name: str, contact: str, source: str = "", stage: str = "NEW_LEAD",
             score: float = 0.0, expected_value: float = 0.0, notes: str = "") -> ToolResult:
        try:
            lead = self.repo.upsert_lead(
                name=name, contact=contact, source=source, stage=stage,
                score=score, expected_value=expected_value, notes=notes,
            )
            return ToolResult(success=True, data=lead)
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))
