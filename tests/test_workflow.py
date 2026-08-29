from app.agents.workflow import Stage, approve_action, execute_approved, prepare_action


def test_high_impact_action_waits_for_approval():
    pending = prepare_action("purchase", "Buy 10 units", 1000)
    assert pending.stage == Stage.APPROVAL
    assert not execute_approved(pending)


def test_approved_action_can_complete():
    pending = prepare_action("purchase", "Buy 10 units", 1000)
    approve_action(pending)
    assert pending.stage == Stage.EXECUTION
    assert execute_approved(pending)
    assert pending.stage == Stage.COMPLETE


def test_read_only_action_skips_approval():
    pending = prepare_action("research", "Find suppliers")
    assert pending.stage == Stage.EXECUTION
    assert execute_approved(pending)
