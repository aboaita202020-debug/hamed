from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StockAgent:
    name: str
    specialty: str
    capabilities: tuple[str, ...]
    mode: str = "research_and_analysis"
    prediction_note: str = "probabilistic_analysis_only; no guaranteed future price prediction"

GROUPS: dict[str, tuple[int, tuple[str, ...]]] = {
    "market_structure": (15, ("market structure","indices","sectors","breadth","liquidity")),
    "fundamental_analysis": (25, ("financial statements","valuation","earnings","cash flow","quality")),
    "technical_analysis": (25, ("price action","trend","momentum","volume","technical indicators")),
    "quantitative_research": (20, ("statistics","factor models","time series","backtesting","signal research")),
    "macro_economics": (15, ("inflation","interest rates","GDP","central banks","FX")),
    "risk_management": (20, ("position sizing","drawdown","stress testing","VaR","risk controls")),
    "portfolio_research": (15, ("asset allocation","diversification","correlation","portfolio construction")),
    "derivatives_research": (15, ("options","futures","volatility","Greeks","hedging")),
    "news_and_sentiment": (15, ("news analysis","earnings calls","sentiment","event detection","source verification")),
    "market_microstructure": (10, ("order books","spreads","slippage","execution research","liquidity")),
    "compliance_and_governance": (10, ("disclosures","market rules","auditability","conflicts","research governance")),
    "strategy_validation": (5, ("hypothesis testing","walk-forward tests","benchmarking","robustness","model risk")),
    "signal_fusion": (10, ("multi-factor signals","ensemble models","regime detection","confidence calibration","signal ranking")),
}

STOCK_AGENTS: list[StockAgent] = []
for group,(count,caps) in GROUPS.items():
    for i in range(1,count+1):
        STOCK_AGENTS.append(StockAgent(
            name=f"ORVIA-Stock-{group.replace('_','-')}-{i:03d}",
            specialty=group,
            capabilities=caps,
        ))

STOCK_TARGET = 200

def stock_status() -> dict[str, Any]:
    return {
        "total": len(STOCK_AGENTS),
        "target": STOCK_TARGET,
        "groups": {k:v[0] for k,v in GROUPS.items()},
        "mode": "research_and_analysis",
        "autonomous_trading": False,
        "human_approval_required_for_orders": True,
    }

def select_stock_agents(topic: str, limit: int = 20) -> list[StockAgent]:
    t = topic.lower()
    keywords = {
        "technical": "technical_analysis", "chart": "technical_analysis",
        "fundamental": "fundamental_analysis", "valuation": "fundamental_analysis",
        "quant": "quantitative_research", "backtest": "quantitative_research",
        "macro": "macro_economics", "interest": "macro_economics",
        "risk": "risk_management", "portfolio": "portfolio_research",
        "options": "derivatives_research", "futures": "derivatives_research",
        "news": "news_and_sentiment", "sentiment": "news_and_sentiment",
        "order": "market_microstructure", "liquidity": "market_microstructure",
        "compliance": "compliance_and_governance", "data": "quantitative_research", "forecast": "signal_fusion", "signal": "signal_fusion",
    }
    chosen_group = next((g for k,g in keywords.items() if k in t), None)
    pool = [a for a in STOCK_AGENTS if a.specialty == chosen_group] if chosen_group else STOCK_AGENTS
    return pool[:max(1, min(limit, len(pool)))]

assert len(STOCK_AGENTS) == STOCK_TARGET
assert sum(v[0] for v in GROUPS.values()) == STOCK_TARGET
assert len({a.name for a in STOCK_AGENTS}) == STOCK_TARGET
