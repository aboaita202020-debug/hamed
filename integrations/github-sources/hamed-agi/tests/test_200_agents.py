from app.agent_bus import agent_bus
from app.agents import DEFAULT_AGENTS, DEPARTMENT_COUNTS
from app.orchestrator import orchestrator


def test_hamed_has_2020_unique_agents():
    assert len(DEFAULT_AGENTS) == 2020
    assert len({a.name for a in DEFAULT_AGENTS}) == 2020

def test_department_counts_sum_to_2020():
    assert sum(DEPARTMENT_COUNTS.values()) == 2020

def test_orchestrator_has_2020_agents():
    assert len(orchestrator.agents) == 2020

def test_agents_can_talk_to_each_other():
    before = len(agent_bus.messages)
    results = orchestrator.collaborate("kids English YouTube daily production", ["research", "analytics", "reporting"])
    assert len(results) == 3
    assert len(agent_bus.messages) > before


def test_discovery_fallback_produces_public_business_targets(monkeypatch):
    from app import prospect_discovery as pd
    monkeypatch.setattr(pd, "_provider_urls", lambda query: ["https://unreachable.invalid/search"])
    monkeypatch.setattr(pd, "_search", lambda url: (_ for _ in ()).throw(OSError("network unavailable")))
    targets = pd.discover_prospects(3, ["online store ecommerce"])
    assert len(targets) == 3
    assert all(t.startswith("https://") for t in targets)
    assert pd.discovery_runtime_status()["fallback_used"] is True


def test_discovery_runtime_reports_provider_failures(monkeypatch):
    from app import prospect_discovery as pd
    monkeypatch.setattr(pd, "_provider_urls", lambda query: ["https://unreachable.invalid/search"])
    monkeypatch.setattr(pd, "_search", lambda url: (_ for _ in ()).throw(OSError("blocked")))
    pd.discover_prospects(1, ["shop"])
    status = pd.discovery_runtime_status()
    assert status["status"] == "ok"
    assert status["found"] == 1
    assert status["providers"]["unreachable.invalid"]["status"] == "error"


def test_research_gateway_fallback_provides_corroborated_identity(monkeypatch):
    from app.research import Evidence, research

    monkeypatch.setattr(
        research,
        "_gateway_research",
        lambda url: Evidence(
            url=url,
            collected_at="now",
            status_code=200,
            title="example.com",
            notes="research_gateway: search_corroboration=bing,google; identity_only=true; page_content_not_verified",
            evidence_type="search_corroborated",
        ),
    )
    monkeypatch.setattr(
        "app.research.urlopen",
        lambda *args, **kwargs: (_ for _ in ()).throw(OSError("direct blocked")),
    )
    evidence = research.fetch("https://example.com/")
    assert evidence.evidence_type == "search_corroborated"
    assert evidence.status_code == 200
    assert "identity_only=true" in evidence.notes


def test_research_retries_transient_connection_errors(monkeypatch):
    from app.research import PublicResearch

    calls = {"count": 0}

    class FakeResponse:
        status = 200
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def read(self, *args):
            return b"<title>Example</title>"

    def flaky_urlopen(*args, **kwargs):
        calls["count"] += 1
        if calls["count"] < 3:
            raise OSError(111, "Connection refused")
        return FakeResponse()

    monkeypatch.setattr("app.research.urlopen", flaky_urlopen)
    monkeypatch.setattr("app.research.time.sleep", lambda *_: None)
    evidence = PublicResearch().fetch("https://example.com/")
    assert evidence.evidence_type == "direct_page"
    assert evidence.status_code == 200
    assert calls["count"] == 3


def test_research_gateway_normalizes_google_redirect_results(monkeypatch):
    from app.research import PublicResearch

    gateway = PublicResearch()
    pages = {
        "duckduckgo.com": ["https://html.duckduckgo.com/html/?uddg=https%3A%2F%2Fexample.com%2Fshop"],
        "bing.com": ["https://www.bing.com/ck/a?u=https%3A%2F%2Fexample.com%2Fshop"],
        "google.com": ["https://www.google.com/url?q=https%3A%2F%2Fexample.com%2Fshop&sa=U"],
    }
    monkeypatch.setattr(
        gateway,
        "_search_provider",
        lambda provider_url: pages[next(host for host in pages if host in provider_url)],
    )

    evidence = gateway._gateway_research("https://example.com/shop")
    assert evidence is not None
    assert evidence.evidence_type == "search_corroborated"
    assert "google.com" in evidence.notes
    assert "identity_only=true" in evidence.notes
