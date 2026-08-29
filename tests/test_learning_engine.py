from app.agents.learning_engine import CommercialLearningEngine, LearningRecord, Skill


def test_learning_engine_records_lessons_and_outcomes():
    engine = CommercialLearningEngine()
    engine.learn(LearningRecord(Skill.SALES, "Lead with value before discount", source="training"))
    engine.learn_from_outcome(Skill.NEGOTIATION, "Trade price for larger quantity", "customer accepted", True)
    engine.learn_from_outcome(Skill.AFFILIATE, "Prefer high-conversion offer over highest commission", "low conversion", False)

    assert len(engine.lessons()) == 3
    assert engine.playbook(Skill.NEGOTIATION)[0] == "Trade price for larger quantity"
    summary = engine.summarize()
    assert summary["total_lessons"] == 3
    assert summary["successful_outcomes"] == 1
    assert summary["failed_outcomes"] == 1
