from app.execution import execution_loop
from app.planner import planner


def test_planner_builds_safe_commercial_plan():
    mission = planner.plan("audit an e-commerce store")
    assert mission.status == "planned"
    assert "web_research" in mission.actions
    assert "sentinel_authorized_scan" not in mission.actions


def test_planner_adds_authorized_security_step_for_target():
    mission = planner.plan("security assessment", target="https://example.com")
    assert "sentinel_authorized_scan" in mission.actions


def test_execution_loop_blocks_unauthorized_security_without_stopping_safe_steps():
    result = execution_loop.run(
        "security assessment",
        target="https://example.com",
        authorized=False,
        dry_run=True,
    )
    assert result["status"] in {"completed", "degraded"}
    assert any(x["status"] == "blocked" for x in result["blocked_steps"])
