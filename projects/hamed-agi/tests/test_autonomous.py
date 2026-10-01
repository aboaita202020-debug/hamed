from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.autonomous import AutonomousCommercialAgent, autonomous_agent
from app.main import app
from app.prospect_discovery import discover_prospects


def test_prospect_discovery_filters_and_limits(monkeypatch):
    monkeypatch.setattr("app.prospect_discovery.urlopen", lambda *args, **kwargs: type("R", (), {"__enter__": lambda s: s, "__exit__": lambda *a: None, "read": lambda s: b'<a href="https://good.example/store">good</a><a href="https://www.facebook.com/x">blocked</a>'})())
    found = discover_prospects(max_targets=1, queries=["test"])
    assert found == ["https://good.example/store"]


def test_prospect_discovery_falls_back_to_bing(monkeypatch):
    calls = []

    def fake_urlopen(request, **kwargs):
        calls.append(request.full_url)
        if "duckduckgo.com" in request.full_url:
            raise OSError("DuckDuckGo unavailable")
        return type("R", (), {
            "__enter__": lambda s: s,
            "__exit__": lambda *a: None,
            "read": lambda s: b'<a href="https://shop.example/products">shop</a>',
        })()

    monkeypatch.setattr("app.prospect_discovery.urlopen", fake_urlopen)
    found = discover_prospects(max_targets=1, queries=["test"])
    assert found == ["https://shop.example/products"]
    assert any("bing.com/search" in url for url in calls)


def test_non_business_pages_are_rejected_before_offer_creation():
    agent = AutonomousCommercialAgent()

    government = SimpleNamespace(
        url="https://www.trade.gov/country-commercial-guides/egypt-ecommerce",
        status_code=200,
        title="Egypt eCommerce | Country Commercial Guide",
        notes="public evidence collected",
    )
    directory = SimpleNamespace(
        url="https://www.wmtips.com/technologies/e-commerce/country/eg/",
        status_code=200,
        title="E-commerce Technologies in Egypt",
        notes="public evidence collected",
    )
    real_business = SimpleNamespace(
        url="https://example.com/store",
        status_code=200,
        title="Example Prospect",
        notes="public evidence collected",
    )

    assert agent._is_qualified_prospect(government)[0] is False
    assert agent._is_qualified_prospect(directory)[0] is False
    assert agent._is_qualified_prospect(real_business)[0] is True


def test_research_classifies_connection_errors():
    from app.research import PublicResearch

    assert PublicResearch._network_error_code(OSError(111, "Connection refused")) == "connection_refused"
    assert PublicResearch._network_error_code(OSError(99, "Cannot assign requested address")) == "cannot_assign_address"
    assert PublicResearch._network_error_code(TimeoutError("timed out")) == "timeout"


def test_identity_only_search_corroboration_is_not_a_qualified_lead():
    agent = AutonomousCommercialAgent()
    evidence = SimpleNamespace(
        url="https://example.com/store",
        status_code=200,
        title="Example Prospect",
        notes="research_gateway: search_corroboration=google.com; identity_only=true; page_content_not_verified",
        evidence_type="search_corroborated",
    )
    qualified, reason = agent._is_qualified_prospect(evidence)
    assert qualified is False
    assert reason == "identity_only_page_not_verified"


def test_autonomous_status_and_cycle(monkeypatch):
    monkeypatch.setenv("ORVIA_AUTONOMOUS_ENABLED", "true")
    monkeypatch.delenv("ORVIA_PROSPECT_URLS", raising=False)
    monkeypatch.setattr("app.autonomous.discover_prospects", lambda max_targets: ["https://example.com"])

    def fake_fetch(url):
        return SimpleNamespace(
            url=url,
            collected_at="2026-01-01T00:00:00+00:00",
            status_code=200,
            title="Example Prospect",
            notes="test evidence",
        )

    monkeypatch.setattr("app.autonomous.research.fetch", fake_fetch)
    autonomous_agent.enabled = True

    client = TestClient(app)
    status = client.get("/api/v1/autonomous/status")
    assert status.status_code == 200
    assert status.json()["enabled"] is True

    run = client.post("/api/v1/autonomous/run", json={"objective": "test commercial scan"})
    assert run.status_code == 200
    assert run.json()["status"] == "completed"
    assert run.json()["leads"]
    assert run.json()["offers"]
