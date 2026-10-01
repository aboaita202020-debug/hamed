from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class WhaleSignal:
    asset: str
    direction: str
    strength: float
    evidence: tuple[str, ...]
    confidence: float
    caveats: tuple[str, ...]

class WhaleSignalEngine:
    """Turns observable large-flow evidence into testable probabilistic signals.
    It does not identify private owners, use stolen data, or guarantee future prices."""
    def analyze(self, asset: str, evidence: list[dict[str, Any]]) -> dict[str, Any]:
        usable = [e for e in evidence if e.get("source") and e.get("metric") is not None]
        if not usable:
            return {"asset": asset, "status": "insufficient_data", "signal": None}
        buy = sum(float(e.get("buy_pressure", 0)) for e in usable)
        sell = sum(float(e.get("sell_pressure", 0)) for e in usable)
        total = buy + sell
        balance = 0.0 if total == 0 else (buy - sell) / total
        direction = "bullish_bias" if balance > 0.2 else "bearish_bias" if balance < -0.2 else "mixed"
        strength = min(1.0, abs(balance))
        confidence = min(0.95, 0.35 + 0.1 * len(usable) + 0.4 * strength)
        return {
            "asset": asset,
            "status": "signal_generated",
            "direction": direction,
            "strength": round(strength, 4),
            "confidence": round(confidence, 4),
            "evidence_count": len(usable),
            "evidence": usable,
            "probabilistic_only": True,
            "guaranteed_price_prediction": False,
        }

def whale_engine_status() -> dict[str, Any]:
    return {"engine": "WhaleSignalEngine", "probabilistic_only": True, "authorized_public_data_only": True}
