from app.services.mission_runtime import MissionRuntime


def test_mission_is_durable_and_deduplicated(tmp_path):
    path = tmp_path / "missions.json"
    runtime = MissionRuntime(str(path))
    first = runtime.submit("Find customers", ["Research stores", "Prepare offer"])
    second = runtime.submit("Find customers", ["different task"])
    assert first["id"] == second["id"]
    restored = MissionRuntime(str(path)).get(first["id"])
    assert restored["goal"] == "Find customers"
    assert len(restored["tasks"]) == 2


def test_mission_runs_one_pending_task_and_persists_result(tmp_path):
    runtime = MissionRuntime(str(tmp_path / "missions.json"))
    mission = runtime.submit("Grow sales", ["Analyze demand", "Prepare outreach"])
    result = runtime.run_once(mission["id"], lambda task: {"task": task, "ok": True})
    assert result["tasks"][0]["status"] == "completed"
    assert result["status"] == "pending"
    restored = MissionRuntime(str(tmp_path / "missions.json")).get(mission["id"])
    assert restored["tasks"][0]["result"]["ok"] is True


def test_mission_failure_is_recorded_without_crashing(tmp_path):
    runtime = MissionRuntime(str(tmp_path / "missions.json"))
    mission = runtime.submit("Test failure", ["Break safely"])
    result = runtime.run_once(mission["id"], lambda task: 1 / 0)
    assert result["status"] == "failed"
    assert result["tasks"][0]["status"] == "failed"
    assert result["tasks"][0]["result"]["type"] == "ZeroDivisionError"
