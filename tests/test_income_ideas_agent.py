import unittest

from app.db.database import Database
from app.agents.orchestrator import HamedOrchestrator


class TestIncomeIdeasAgent(unittest.TestCase):
    def setUp(self):
        self.orch = HamedOrchestrator(db=Database(path=":memory:"))

    def test_catalog_is_available(self):
        outcome = self.orch.dispatch("income_ideas_agent", {})
        self.assertTrue(outcome.result.success)
        self.assertEqual(outcome.result.data["status"], "catalog_ready")
        self.assertEqual(outcome.result.data["count"], 95)

    def test_get_idea(self):
        outcome = self.orch.dispatch("income_ideas_agent", {"action": "get", "id": 18})
        self.assertTrue(outcome.result.success)
        self.assertEqual(outcome.result.data["idea"]["id"], 18)
        self.assertIn("lead_generation_agent", outcome.result.data["idea"]["agents"])

    def test_search_ideas(self):
        outcome = self.orch.dispatch("income_ideas_agent", {"action": "search", "query": "Affiliate", "limit": 10})
        self.assertTrue(outcome.result.success)
        self.assertGreaterEqual(outcome.result.data["count"], 1)


if __name__ == "__main__":
    unittest.main()
