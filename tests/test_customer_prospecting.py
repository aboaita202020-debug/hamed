from app.services.customer_prospecting import CustomerProspectingEngine


def test_digital_gap_creates_qualified_service_opportunity():
    engine = CustomerProspectingEngine()
    result = engine.assess({
        "post": "We sell clothes but we don't have a website or online store yet.",
        "evidence": ["public business post"],
    })
    assert result.qualified is True
    assert result.opportunity_type == "digital_presence_gap"
    assert result.recommended_service == "website_or_ecommerce_store"
    assert result.outreach_allowed is True


def test_missing_evidence_blocks_outreach():
    result = CustomerProspectingEngine().assess({"post": "We need more sales."})
    assert result.qualified is False
    assert result.outreach_allowed is False


def test_outreach_does_not_make_guaranteed_results_claims():
    engine = CustomerProspectingEngine()
    result = engine.assess({"about": "No website yet", "evidence": ["public profile"]})
    outreach = engine.build_outreach(name="Customer", assessment=result)
    assert outreach["approved"] is True
    assert "guarantee" not in outreach["message"].lower()
    assert "public" in outreach["message"].lower()
