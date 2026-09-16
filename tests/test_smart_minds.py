from app.agents.smart_minds import SMART_MINDS, list_smart_minds


def test_smart_mind_catalog_has_expected_business_capabilities():
    minds = list_smart_minds()
    assert len(minds) >= 15
    ids = {mind["id"] for mind in minds}
    for required in {
        "central_council",
        "opportunity_hunter",
        "sales",
        "purchasing",
        "negotiation",
        "customer_psychology",
        "marketing",
        "affiliate",
        "b2b",
        "website_factory",
        "lead_discovery",
        "research",
        "learning",
        "memory",
        "execution",
        "risk_guard",
    }:
        assert required in ids


def test_every_mind_has_ui_metadata():
    assert SMART_MINDS
    for mind in SMART_MINDS:
        assert mind["name"]
        assert mind["ar"]
        assert mind["icon"]
        assert mind["description"]
