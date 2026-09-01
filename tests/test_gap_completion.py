import os
from pathlib import Path

from app.agents.registry import AGENT_REGISTRY, LEARNING_COUNCIL, CLIENT_RESEARCH_AGENTS
from app.agents.execution import AgentExecutor
from app.services import (
    CRM, EducationCouncil, OpportunityEngine, PackageEngine, OfferEngine,
    NegotiationEngine, QRMenu, ReputationEngine, SalesMessageEngine,
    ServiceCatalog, WebsiteAnalyzer, StoreAnalyzer, RestaurantGrowthEngine,
)


def test_agent_registry_is_real_and_executable():
    assert len(AGENT_REGISTRY) >= 80
    assert len(AGENT_REGISTRY) == len(set(AGENT_REGISTRY))
    executor = AgentExecutor()
    contracts = executor.contracts()
    assert len(contracts) == len(AGENT_REGISTRY)
    for c in contracts:
        assert all([c.id, c.name, c.role, c.description, c.capabilities, c.tasks, c.permissions])
        assert c.input_schema["required"] == ["task"]
        assert executor.execute(c.id, "test task")["status"] == "completed"


def test_councils_have_required_members():
    assert len(LEARNING_COUNCIL) == 5
    assert len(CLIENT_RESEARCH_AGENTS) == 5
    assert "psychology-research" in LEARNING_COUNCIL
    assert "sales-science" in LEARNING_COUNCIL
    assert "strategy-research" in LEARNING_COUNCIL


def test_business_engines_only_return_supplied_evidence():
    business = {"evidence": ["public evidence"], "problems": ["slow mobile UX"], "opportunities": ["mobile optimization"]}
    assert OpportunityEngine().analyze(business)["evidence"] == business["evidence"]
    assert WebsiteAnalyzer().analyze({"evidence": ["ux evidence"], "ux": "poor"})["evidence"] == ["ux evidence"]
    assert StoreAnalyzer().analyze({"evidence": ["checkout evidence"], "checkout": "needs review"})["evidence"] == ["checkout evidence"]
    assert RestaurantGrowthEngine().analyze({"evidence": ["menu evidence"]})["evidence"] == ["menu evidence"]


def test_qr_menu_is_updateable_and_generates_valid_svg():
    qr = QRMenu("https://example.test")
    url = qr.create("abc", {"title": "Menu", "items": ["Tea"]})
    assert url.endswith("/menu/abc")
    svg = qr.generate("abc")
    assert svg.startswith(b"<?xml") or b"<svg" in svg
    qr.update("abc", {"title": "Updated", "items": ["Coffee"]})
    assert qr.page("abc")["content"]["title"] == "Updated"
    assert qr.page("missing")["status"] == "not_found"


def test_reputation_sales_package_offer_negotiation_and_crm():
    reputation = ReputationEngine().analyze([{"rating": 5, "text": "excellent service"}, {"rating": 2, "text": "slow service"}])
    assert reputation["count"] == 2
    msg = SalesMessageEngine().generate({"name": "Business", "problem": "slow mobile UX", "service": "website optimization", "evidence": ["public audit"]})
    assert "slow mobile UX" in msg["message"]
    catalog = ServiceCatalog()
    package = PackageEngine().build(["website-optimization", "qr-menu"], catalog)
    offer = OfferEngine().create(package, price=1000, deposit=100, timeline="7 days")
    assert offer["deposit"] == 100
    assert NegotiationEngine().negotiate(price=1000, minimum_price=900, discount=0.05, deposit_percentage=0.1, allowed_deliverables=package["deliverables"], requested_deliverables=package["deliverables"])["accepted"]
    assert not NegotiationEngine().negotiate(price=1000, minimum_price=900, discount=0.2, deposit_percentage=0.1, allowed_deliverables=package["deliverables"], requested_deliverables=package["deliverables"])["accepted"]
    crm = CRM(); record = crm.create(deal_value=1000); assert crm.transition(record["lead_id"], "qualified")["status"] == "qualified"


def test_education_requires_evidence_and_confidence():
    council = EducationCouncil()
    result = council.process("claim", "https://example.test/source", "quoted evidence", 0.8)
    assert result["knowledge"].source.startswith("https://")
    assert result["knowledge"].confidence == 0.8
    try:
        council.process("claim", "", "evidence", 0.8)
    except ValueError:
        pass
    else:
        raise AssertionError("missing source must fail")


def test_no_secret_literals_in_python_source():
    forbidden = ("sk-proj-", "sk-ant-", "AIzaSy", "xoxb-")
    for path in Path(".").rglob("*.py"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert not any(token in text for token in forbidden), path
