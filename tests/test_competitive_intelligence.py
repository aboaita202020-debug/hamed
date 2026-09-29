from app.services.competitive_intelligence import CompetitiveIntelligenceEngine


def test_competitive_intelligence_maps_public_gap_to_service():
    engine = CompetitiveIntelligenceEngine()
    result = engine.analyze(
        "Example Store",
        [
            {
                "type": "content",
                "signal": "Product pages have no short-form demonstration videos",
                "evidence": "Public product pages checked",
                "impact": "conversion_friction",
                "confidence": 0.9,
                "gap": "Weak product demonstration",
            },
            {
                "type": "pricing",
                "signal": "Bundle pricing is unclear",
                "evidence": "Public pricing page",
                "gap": "Offer clarity",
            },
        ],
    )
    assert len(result["findings"]) == 2
    assert result["opportunities"][0]["recommended_service"] == "Content and AI-UGC production"
    assert result["evidence_policy"] == "public_observable_only"
    assert "PREPARE_PERSONALIZED_OUTREACH" in result["workflow"]


def test_competitive_intelligence_rejects_unverified_signal():
    engine = CompetitiveIntelligenceEngine()
    result = engine.analyze(
        "Example Store",
        [{"type": "unknown", "signal": "guess", "evidence": "none"}],
    )
    assert result["findings"] == []
    assert result["opportunities"] == []
