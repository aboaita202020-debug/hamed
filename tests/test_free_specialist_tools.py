from app.ai_universal_hub import health, status, find_tools, route

def test_250_free_specialist_tools_are_registered():
    data = health()
    assert data["specialist_free_tools"] == 250
    assert data["registry_size"] >= 250

def test_specialist_routing_is_capability_specific():
    assert route("lead_finder")["selected"]["id"] == "free-lead_finder"
    assert route("speech_to_text")["selected"]["id"] == "free-speech_to_text"
    assert route("store_auditor")["selected"]["id"] == "free-store_auditor"

def test_categories_cover_commercial_work():
    categories = status()["categories"]
    for category in ("research", "sales", "marketing", "ecommerce", "coding", "business_ops"):
        assert category in categories
