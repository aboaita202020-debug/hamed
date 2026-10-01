from app.whale_agents import WHALE_AGENTS, select_whale_agents, whale_status
from app.whale_signal_engine import WhaleSignalEngine


def test_whale_agents_exact_count():
    assert len(WHALE_AGENTS) == 20
    assert len({a.name for a in WHALE_AGENTS}) == 20
    assert sum(whale_status()["groups"].values()) == 20
    assert select_whale_agents("large volume and order flow", 5)

def test_whale_signal_engine():
    result = WhaleSignalEngine().analyze("TEST", [
        {"source":"public_feed","metric":"volume","buy_pressure":80,"sell_pressure":20},
        {"source":"public_feed","metric":"flow","buy_pressure":60,"sell_pressure":40},
    ])
    assert result["status"] == "signal_generated"
    assert result["probabilistic_only"] is True
    assert result["guaranteed_price_prediction"] is False
