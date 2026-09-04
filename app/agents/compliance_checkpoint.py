"""External compliance checkpoint for revenue opportunities.

Gate 5 must not be self-certified by the revenue engine. Opportunities that
cross configurable value/frequency thresholds are placed in a human-review
queue before autonomous commercial execution. The checkpoint never claims
that an opportunity is lawful; it records evidence and requires an explicit
review decision from an authorized human reviewer.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import os
from typing import Any, Optional


@dataclass(frozen=True)
class ComplianceReview:
    opportunity_id: str
    required: bool
    status: str
    reason: str
    evidence: Any
    value: float
    occurrence_count: int
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ExternalComplianceCheckpoint:
    """Require independent human review for high-value/repeated opportunities."""

    def __init__(self, audit_path: Optional[str] = None) -> None:
        self.value_threshold = self._float_env("HAMED_COMPLIANCE_REVIEW_VALUE", 5000.0)
        self.frequency_threshold = self._int_env("HAMED_COMPLIANCE_REVIEW_FREQUENCY", 3)
        self.audit_path = audit_path or os.getenv("HAMED_COMPLIANCE_AUDIT_PATH", "")

    def evaluate(self, opportunity: dict[str, Any]) -> ComplianceReview:
        opportunity_id = str(opportunity.get("id") or opportunity.get("opportunity_id") or "unknown")
        evidence = opportunity.get("evidence") or opportunity.get("summary")
        value = max(0.0, self._number(opportunity.get("expected_profit", opportunity.get("deal_value", 0))))
        occurrence_count = max(0, self._int(opportunity.get("occurrence_count", opportunity.get("frequency", 0))))
        explicit = bool(opportunity.get("requires_external_compliance_review"))
        required = explicit or value >= self.value_threshold or occurrence_count >= self.frequency_threshold
        if required:
            reason = "threshold crossed: independent human compliance review required"
            status = "pending_review"
        else:
            reason = "below external-review threshold; normal policy gates still apply"
            status = "not_required"
        review = ComplianceReview(
            opportunity_id=opportunity_id,
            required=required,
            status=status,
            reason=reason,
            evidence=evidence,
            value=round(value, 2),
            occurrence_count=occurrence_count,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._record(review)
        return review

    @staticmethod
    def approve(review: ComplianceReview, reviewer: str) -> dict[str, Any]:
        reviewer = str(reviewer).strip()
        if not reviewer:
            raise ValueError("reviewer is required")
        if review.required:
            return {**review.to_dict(), "status": "approved", "reviewer": reviewer,
                    "reviewed_at": datetime.now(timezone.utc).isoformat()}
        return {**review.to_dict(), "status": "not_required", "reviewer": reviewer}

    @staticmethod
    def _float_env(name: str, default: float) -> float:
        try:
            return max(0.0, float(os.getenv(name, str(default))))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _int_env(name: str, default: int) -> int:
        try:
            return max(1, int(os.getenv(name, str(default))))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _number(value: Any) -> float:
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _int(value: Any) -> int:
        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0

    def _record(self, review: ComplianceReview) -> None:
        if not self.audit_path:
            return
        directory = os.path.dirname(self.audit_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(self.audit_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(review.to_dict(), ensure_ascii=False) + "\n")
