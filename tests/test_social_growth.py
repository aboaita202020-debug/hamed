from app.services.social_growth import SocialGrowthEngine
from app.services.platform import ServiceCatalog


def test_social_growth_plan_and_queue():
    engine = SocialGrowthEngine()
    plan = engine.plan(platform="instagram", goal="followers", audience="Egyptian customers")
    assert plan.platform == "instagram"
    assert "create_content_calendar" in plan.actions
    queue = engine.action_queue(plan, connected=False)
    assert queue
    assert all(item["status"] == "waiting_for_authorized_connection" for item in queue)


def test_social_growth_services_exist():
    catalog = ServiceCatalog()
    ids = {s.service_id for s in catalog.all()}
    assert {"social-media-management", "content-production", "social-growth", "social-lead-generation"}.issubset(ids)


def test_audit_preserves_evidence_without_inventing():
    result = SocialGrowthEngine().audit({"platform": "facebook", "followers": 1200, "evidence": ["public analytics"]})
    assert result["followers"] == 1200
    assert result["evidence"] == ["public analytics"]
    assert result["engagement_rate"] is None
