from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_orvia_public_control_routes_are_registered_and_live():
    for path in (
        "/health",
        "/readiness",
        "/status",
        "/dashboard",
        "/openapi.json",
        "/ai-hub",
        "/ai-hub/health",
        "/providers",
        "/scout",
        "/agents",
        "/minds",
        "/opportunities",
        "/revenue",
        "/crm",
        "/youtube",
    ):
        response = client.get(path)
        assert response.status_code == 200, (path, response.text)


def test_ai_hub_has_65_tools_and_routes_by_capability():
    hub = client.get("/ai-hub").json()
    assert hub["hub"]["total"] >= 65
    assert hub["hub"]["categories"]["reasoning"] >= 1

    search = client.get("/ai-hub/search", params={"capability": "web-search"}).json()
    assert search["results"]

    route = client.get("/ai-hub/route", params={"capability": "web-search"}).json()
    assert route["selected"] is not None


def test_scout_and_minds_do_not_expose_secret_values():
    scout = client.get("/scout").json()
    assert scout["health"]["secrets_exposed"] is False
    assert any(item["id"] == "freellmapi" for item in scout["providers"])

    minds = client.get("/minds").json()
    assert minds["count"] >= 200
    assert {"identity", "role", "capabilities", "provider"} <= minds["minds"][0].keys()
