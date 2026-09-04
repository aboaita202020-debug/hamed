from app.agents.opportunity_hunter import OpportunityHunter
from app.services import SupplierDatabase, SupplierRecord, DigitalDeliveryEngine


def test_supplier_database_requires_evidence_and_deduplicates():
    db = SupplierDatabase()
    record = db.upsert(name="Supplier A", category="food", evidence=["https://supplier.test"], products=["sugar"], country="Egypt", confidence=.9)
    same = db.upsert(name="Supplier A", category="food", evidence=["https://supplier.test/page"], products=["sugar"])
    assert record.supplier_id == same.supplier_id
    assert len(db.search(category="food", product="sugar")) == 1
    assert len(db.export()) == 1


def test_digital_delivery_builds_and_requires_authorized_deployment():
    engine = DigitalDeliveryEngine()
    store = engine.build(business_name="Test Store", project_type="store")
    assert "checkout" in store["pages"]
    plan = engine.deployment_plan(store)
    assert plan["deployment_authorized"] is False
    assert "human_approval" in plan["steps"]


def test_opportunity_hunter_discovers_and_requires_evidence_for_outreach():
    class DummyResearch:
        def research(self, query):
            return type("R", (), {"findings": "verified supplier evidence"})()
    class DummyOrchestrator:
        research_agent = DummyResearch()
        sales_message_engine = None
        def commercial_opportunity_plan(self, request):
            return {"research_required": True}
    hunter = OpportunityHunter(DummyOrchestrator(), SupplierDatabase())
    item = hunter.discover(source="public_post", demand="عاوز 15000 كيس سكر", evidence=["public post"])
    assert item["category"] == "food"
    result = hunter.research(item["opportunity_id"])
    assert result["research"] == "verified supplier evidence"
    plan = hunter.plan(item["opportunity_id"])
    assert plan["plan"]["research_required"] is True
