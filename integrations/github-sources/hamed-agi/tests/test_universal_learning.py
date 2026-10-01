from app.learning_sprint import learning_sprint
from app.rd_agents import RD_AGENTS, rd_status
from app.universal_learning import universal_learning


def test_exact_500_rd_agents():
    assert len(RD_AGENTS) == 500
    assert len({a.name for a in RD_AGENTS}) == 500
    assert rd_status()["github_discovery_agents"] == 100

def test_universal_source_catalog():
    families = {s.family for s in universal_learning.sources}
    assert {"web","research","universities","youtube","books","github","business_leaders","official_docs"} <= families

def test_learning_verification_gate():
    item = universal_learning.record_knowledge("marketing","test","research","claim",confidence=0.8)
    assert universal_learning.verify(item, supporting_sources=2)["verified"] is True
    blocked = universal_learning.teach_network({**item, "verified": False}, ["learning"])
    assert blocked["status"] == "blocked"

def test_60_minute_sprint():
    result = learning_sprint.run()
    assert result["timebox_minutes"] == 60
    assert "marketing_psychology" in result["domains"]
