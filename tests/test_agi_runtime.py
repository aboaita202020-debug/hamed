import unittest

from app.agi import CognitiveRuntime, PlanStep


class TestCognitiveRuntime(unittest.TestCase):
    def test_low_risk_plan_can_execute(self):
        calls = []
        runtime = CognitiveRuntime(dispatcher=lambda agent, payload: calls.append((agent, payload)) or {"ok": True})
        goal = runtime.create_goal("Find a qualified business opportunity", ["produce a validated opportunity"])
        plan = runtime.build_plan(goal, [PlanStep("Research", "market", {"topic": "ecommerce"})])
        decision = runtime.deliberate(goal, plan, 0.85, ["market demand is testable"])
        result = runtime.execute(goal, plan, decision)
        self.assertEqual(result[0]["status"], "DONE")
        self.assertEqual(calls[0][0], "market")

    def test_high_risk_plan_waits_for_approval(self):
        runtime = CognitiveRuntime()
        goal = runtime.create_goal("Purchase inventory", ["positive expected margin"])
        plan = runtime.build_plan(goal, [PlanStep("Purchase", "procurement", risk="high")])
        decision = runtime.deliberate(goal, plan, 0.9)
        result = runtime.execute(goal, plan, decision)
        self.assertEqual(result[0]["status"], "WAITING_APPROVAL")

    def test_critique_blocks_low_confidence(self):
        runtime = CognitiveRuntime()
        goal = runtime.create_goal("Test", ["success"])
        plan = runtime.build_plan(goal, [PlanStep("Step", "research")])
        decision = runtime.deliberate(goal, plan, 0.2)
        self.assertFalse(runtime.critique(goal, plan, decision)["passed"])

    def test_learning_record_is_stored(self):
        runtime = CognitiveRuntime()
        record = runtime.learn("Short offers convert better", "three experiments", "positive", 0.8)
        self.assertEqual(record.confidence, 0.8)
        self.assertEqual(len(runtime.learning), 1)


if __name__ == "__main__":
    unittest.main()
