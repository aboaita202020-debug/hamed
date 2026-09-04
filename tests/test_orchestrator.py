import unittest

from app.db.database import Database
from app.agents.orchestrator import HamedOrchestrator


def fake_search_provider(query: str, max_results: int):
    return [
        {"title": "Fake Co needs a website", "url": "http://example.com", "snippet": "...",
         "source": "facebook", "confidence": 0.8},
    ]


class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.db = Database(path=":memory:")
        self.orch = HamedOrchestrator(db=self.db, search_provider=fake_search_provider)

    def test_unknown_agent_returns_error_not_crash(self):
        outcome = self.orch.dispatch("does_not_exist", {})
        self.assertFalse(outcome.result.success)
        self.assertIn("unknown_agent", outcome.result.error)

    def test_opportunity_hunter_creates_opportunities(self):
        outcome = self.orch.dispatch("opportunity_hunter", {"query": "companies without websites"})
        self.assertTrue(outcome.result.success)
        self.assertEqual(len(outcome.result.data), 1)
        self.assertGreater(outcome.result.data[0].opportunity_score, 0)

    def test_reporting_agent_dashboard_snapshot(self):
        snapshot = self.orch.dashboard()
        self.assertIn("leads", snapshot)
        self.assertIn("pipeline", snapshot)

    def test_full_sales_pipeline_flow(self):
        # Create a lead via CRM tool through the registry directly
        result = self.orch.tools.execute(
            actor="test", tool_name="crm_upsert_lead",
            name="Acme Store", contact="acme@example.com", source="facebook",
        )
        self.assertTrue(result.success)
        lead = result.data

        proposal_outcome = self.orch.dispatch(
            "sales_agent",
            {"lead_id": lead.id, "action": "create_proposal",
             "service": "Landing Page", "price": 5000},
        )
        self.assertTrue(proposal_outcome.result.success)
        deal = proposal_outcome.result.data["deal"]
        self.assertEqual(deal.status, "OPEN")

        closed = self.orch.repo.close_deal(deal.id, won=True, actual_revenue=5000)
        self.assertEqual(closed.status, "WON")

        revenue_outcome = self.orch.dispatch("revenue_agent", {})
        self.assertEqual(revenue_outcome.result.data["won_deals"], 1)
        self.assertEqual(revenue_outcome.result.data["actual_revenue"], 5000)

    def tearDown(self):
        self.db.close()


if __name__ == "__main__":
    unittest.main()
