from app.collective_intelligence import collective_intelligence
from app.science_agents import SCIENCE_AGENTS
from app.social_agents import SOCIAL_AGENTS, social_status


def test_science_agents_exact_count():
    assert len(SCIENCE_AGENTS) == 1000
    assert len({a.name for a in SCIENCE_AGENTS}) == 1000
    assert sum(x[1] for x in __import__("app.science_agents", fromlist=["SCIENCE_DOMAINS"]).SCIENCE_DOMAINS) == 1000

def test_social_agents_exact_count():
    assert len(SOCIAL_AGENTS) == 100
    assert len({a.name for a in SOCIAL_AGENTS}) == 100
    assert social_status()["groups"] == {"tiktok_instagram":50,"facebook_youtube":50}

def test_collective_total():
    assert collective_intelligence.total_configured_agents == 2020
    status=collective_intelligence.status()
    assert status["shared_memory"] is True
    assert status["peer_review"] is True
    assert status["help_protocol"] is True


def test_alchemy_specialization():
    from app.science_agents import ALCHEMY_AGENTS, alchemy_status, select_alchemy_agents
    assert len(ALCHEMY_AGENTS) == 100
    assert len({a.name for a in ALCHEMY_AGENTS}) == 100
    assert alchemy_status()["total_science_network"] == 1000
    assert sum(alchemy_status()["allocation"].values()) == 100
    assert select_alchemy_agents("Egyptian alchemy", 10)


def test_stock_agents_exact_count_and_specialization():
    from app.stock_agents import STOCK_AGENTS, select_stock_agents, stock_status
    assert len(STOCK_AGENTS) == 200
    assert len({a.name for a in STOCK_AGENTS}) == 200
    assert stock_status()["total"] == 200
    assert sum(stock_status()["groups"].values()) == 200
    assert select_stock_agents("technical analysis and market data", 10)
