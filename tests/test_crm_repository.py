import unittest

from app.db.database import Database
from app.db.repository import Repository


class TestCRMDeduplication(unittest.TestCase):
    def setUp(self):
        self.db = Database(path=":memory:")
        self.repo = Repository(self.db)

    def test_upsert_creates_new_lead(self):
        lead = self.repo.upsert_lead(name="Acme", contact="acme@example.com", source="facebook")
        self.assertIsNotNone(lead.id)
        self.assertEqual(lead.stage, "NEW_LEAD")

    def test_upsert_same_contact_updates_not_duplicates(self):
        first = self.repo.upsert_lead(name="Acme", contact="acme@example.com", source="facebook")
        second = self.repo.upsert_lead(name="Acme Store", contact="acme@example.com",
                                        source="facebook", stage="QUALIFIED")
        self.assertEqual(first.id, second.id)
        all_leads = self.repo.list_leads()
        self.assertEqual(len(all_leads), 1)
        self.assertEqual(second.stage, "QUALIFIED")

    def test_leads_without_contact_are_not_deduped_against_each_other(self):
        self.repo.upsert_lead(name="Walk-in 1", contact="")
        self.repo.upsert_lead(name="Walk-in 2", contact="")
        # sqlite UNIQUE constraint treats multiple NULLs as distinct
        self.assertEqual(len(self.repo.list_leads()), 2)

    def test_pipeline_metrics_expected_vs_actual(self):
        lead = self.repo.upsert_lead(name="Beta", contact="beta@example.com")
        deal = self.repo.open_deal(lead.id, proposal_id=None, expected_revenue=3000)
        metrics_before = self.repo.pipeline_metrics()
        self.assertEqual(metrics_before["expected_revenue"], 3000)
        self.assertEqual(metrics_before["actual_revenue"], 0)

        self.repo.close_deal(deal.id, won=True, actual_revenue=2800)
        metrics_after = self.repo.pipeline_metrics()
        self.assertEqual(metrics_after["actual_revenue"], 2800)
        self.assertEqual(metrics_after["won_deals"], 1)
        self.assertEqual(metrics_after["close_rate_pct"], 100.0)

    def tearDown(self):
        self.db.close()


if __name__ == "__main__":
    unittest.main()
