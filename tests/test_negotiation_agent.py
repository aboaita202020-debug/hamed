import unittest

from app.db.database import Database
from app.agents.orchestrator import HamedOrchestrator


class TestNegotiationAgent(unittest.TestCase):
    def setUp(self):
        self.db = Database(path=":memory:")
        self.orch = HamedOrchestrator(db=self.db)

    def test_counter_within_floor_is_accepted(self):
        outcome = self.orch.dispatch(
            "negotiation_agent",
            {"target_price": 1000, "counter_offer": 950, "minimum_price": 700},
        )
        self.assertTrue(outcome.result.success)
        self.assertIn(outcome.result.data["decision"], ("accept", "counter"))

    def test_counter_below_floor_escalates_not_accepts(self):
        outcome = self.orch.dispatch(
            "negotiation_agent",
            {"target_price": 1000, "counter_offer": 300, "minimum_price": 700},
        )
        self.assertFalse(outcome.result.success)
        self.assertIn("escalate_to_owner", outcome.result.next_actions)

    def tearDown(self):
        self.db.close()


if __name__ == "__main__":
    unittest.main()
