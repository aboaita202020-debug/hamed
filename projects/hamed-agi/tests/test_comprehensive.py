from fastapi.testclient import TestClient

from app.agents import DEFAULT_AGENTS, SalesAgent
from app.config import settings
from app.crm import CRM, Customer
from app.learning import LearningMemory
from app.main import app
from app.marketing import build_store_offer
from app.models import Mission
from app.opportunities import score_opportunity
from app.opportunity import OpportunityEngine
from app.orchestrator import orchestrator
from app.revenue import RevenueEngine


def test_all_core_modules_and_agents():
    assert len(DEFAULT_AGENTS) >= 15
    assert SalesAgent().run({"objective": "sell"}).status == "ok"
    assert len(orchestrator.run("test")) == len(DEFAULT_AGENTS)
    assert OpportunityEngine().discover(Mission(objective="test"))
    assert score_opportunity("p", ["e1", "e2", "e3"]).score >= 0.65
    assert LearningMemory().record("x", "y", "test", 1.2).confidence == 1.0
    offer = build_store_offer(OpportunityEngine().discover(Mission(objective="x"))[0])
    assert offer.message and offer.evidence

def test_crm_and_revenue():
    crm = CRM()
    crm.upsert(Customer("demo", "contact"))
    assert crm.summary()["customers"] == 1
    revenue = RevenueEngine()
    revenue.record("demo", 100, "EGP", "realized")
    revenue.record("demo", 50, "EGP", "pending")
    assert revenue.total_realized("EGP") == 100

def test_fastapi_and_approval_configuration():
    client = TestClient(app)
    for path in ("/", "/dashboard", "/health", "/readiness", "/status", "/api/v1/providers", "/api/v1/report"):
        assert client.get(path).status_code == 200
    assert client.get("/health").json()["status"] == "ok"
    assert client.get("/readiness").json()["ready"] is True
    assert settings.require_approval_for_financial_actions is True
    assert client.post("/agi/mission", json={"objective": "test"}).json()["status"] == "completed"
