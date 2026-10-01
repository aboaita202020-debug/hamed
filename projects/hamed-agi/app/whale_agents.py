from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class WhaleAgent:
    name: str
    specialty: str
    capabilities: tuple[str, ...]
    mode: str = "research_and_analysis"

WHALE_GROUPS: dict[str, tuple[int, tuple[str, ...]]] = {
    "flow_detection": (3, ("large trade detection","volume anomalies","capital flows","liquidity shifts")),
    "institutional_flow": (3, ("institutional holdings","fund flows","disclosures","institutional activity")),
    "order_flow": (3, ("order flow","bid ask pressure","market depth","execution imbalance")),
    "accumulation_distribution": (3, ("accumulation","distribution","volume price analysis","regime detection")),
    "whale_behavior": (2, ("behavioral patterns","historical flow patterns","event response","anomaly detection")),
    "market_impact": (2, ("market impact","liquidity","slippage","price response")),
    "signal_fusion": (2, ("multi-signal fusion","confidence calibration","cross-agent validation","scenario analysis")),
    "verification_risk": (2, ("false signal detection","data quality","backtesting","risk controls")),
}
WHALE_TARGET = 20
WHALE_AGENTS: list[WhaleAgent] = []
for group, (count, caps) in WHALE_GROUPS.items():
    for i in range(1, count + 1):
        WHALE_AGENTS.append(WhaleAgent(
            name=f"ORVIA-Whale-{group.replace('_','-')}-{i:03d}",
            specialty=group,
            capabilities=caps,
        ))

def whale_status() -> dict[str, Any]:
    return {
        "total": len(WHALE_AGENTS),
        "target": WHALE_TARGET,
        "groups": {k: v[0] for k, v in WHALE_GROUPS.items()},
        "mode": "research_and_analysis",
        "probabilistic_only": True,
        "guaranteed_price_prediction": False,
    }

def select_whale_agents(topic: str, limit: int = 10) -> list[WhaleAgent]:
    t = topic.lower()
    keywords = {
        "flow": "flow_detection", "volume": "flow_detection", "institution": "institutional_flow",
        "fund": "institutional_flow", "order": "order_flow", "depth": "order_flow",
        "accumulation": "accumulation_distribution", "distribution": "accumulation_distribution",
        "whale": "whale_behavior", "behavior": "whale_behavior", "impact": "market_impact",
        "slippage": "market_impact", "signal": "signal_fusion", "risk": "verification_risk",
        "backtest": "verification_risk",
    }
    group = next((g for k, g in keywords.items() if k in t), None)
    pool = [a for a in WHALE_AGENTS if a.specialty == group] if group else WHALE_AGENTS
    return pool[:max(1, min(limit, len(pool)))]

assert len(WHALE_AGENTS) == WHALE_TARGET
assert sum(v[0] for v in WHALE_GROUPS.values()) == WHALE_TARGET
assert len({a.name for a in WHALE_AGENTS}) == WHALE_TARGET
