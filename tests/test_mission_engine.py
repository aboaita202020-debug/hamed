from app.agents.mission_engine import build_mission, infer_domain


def test_infer_domain_and_build_route():
    assert infer_domain("أريد بناء متجر إلكتروني") == "website"
    steps = build_mission("أريد بناء متجر إلكتروني")
    assert steps
    assert steps[0]["capability"] == "audit"
    assert any(step["capability"] == "quality" for step in steps)


def test_sensitive_actions_are_marked_for_approval():
    steps = build_mission("general business goal")
    assert all(step["approval_required"] is False for step in steps)
