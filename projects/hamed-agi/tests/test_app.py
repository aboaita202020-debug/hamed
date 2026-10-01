from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "agi_engine" in body["components"]

def test_readiness():
    response = client.get("/readiness")
    assert response.status_code == 200
    body = response.json()
    assert body["ready"] is True
    assert body["financial_approval_gate"] is True

def test_dashboard():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "ORVIA AGI" in response.text

def test_mission():
    response = client.post("/agi/mission", params={"objective": "find ecommerce opportunities"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["offers"]
    assert body["metadata"]["agents"]

def test_store_audit():
    response = client.post("/agi/store-audit", json={"url": "https://example.com"})
    assert response.status_code == 200
    assert response.json()["status"] == "queued"

def test_revenue_engine():
    from app.revenue import revenue_engine
    revenue_engine.record("demo", 100, "EGP", "realized")
    assert revenue_engine.total_realized("EGP") >= 100
