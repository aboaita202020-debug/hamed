from __future__ import annotations

from dataclasses import dataclass

from .governance import approval_for


@dataclass(frozen=True)
class Decision:
    action: str
    proceed: bool
    approval_required: bool
    reason: str
    confidence: float

class DecisionEngine:
    def evaluate(self, action: str, confidence: float = 0.8, value: float | None = None) -> Decision:
        approval = approval_for(action, value)
        confidence = max(0.0, min(confidence, 1.0))
        proceed = confidence >= 0.65 and not approval.required
        reason = "safe reversible action" if proceed else approval.reason if approval.required else "confidence below execution threshold"
        return Decision(action, proceed, approval.required, reason, confidence)

decision_engine = DecisionEngine()
