import unittest

from app.config import ApprovalLimits
from app.db.database import Database
from app.db.repository import Repository
from app.permissions import PermissionLayer, PermissionCheck, PermissionDecision, ApprovalRequired


class TestPermissionLayer(unittest.TestCase):
    def setUp(self):
        self.db = Database(path=":memory:")
        self.repo = Repository(self.db)
        self.limits = ApprovalLimits(
            max_auto_payment_egp=1000,
            max_auto_purchase_egp=2000,
            max_auto_discount_pct=10,
            max_negotiation_concession_pct=15,
            require_approval_for_contracts=True,
        )
        self.perm = PermissionLayer(self.repo, limits=self.limits)

    def test_always_auto_action(self):
        decision = self.perm.evaluate(PermissionCheck(action="web_research"))
        self.assertEqual(decision, PermissionDecision.AUTO)

    def test_contract_always_needs_approval(self):
        decision = self.perm.evaluate(PermissionCheck(action="sign_contract", is_contract=True))
        self.assertEqual(decision, PermissionDecision.PENDING_APPROVAL)

    def test_payment_under_limit_is_auto(self):
        decision = self.perm.evaluate(PermissionCheck(action="payment", amount_egp=500))
        self.assertEqual(decision, PermissionDecision.AUTO)

    def test_payment_over_limit_needs_approval(self):
        decision = self.perm.evaluate(PermissionCheck(action="payment", amount_egp=5000))
        self.assertEqual(decision, PermissionDecision.PENDING_APPROVAL)

    def test_authorize_raises_when_pending(self):
        with self.assertRaises(ApprovalRequired):
            self.perm.authorize("purchasing_agent", PermissionCheck(action="purchase", amount_egp=9999))

    def test_every_decision_is_audited(self):
        self.perm.evaluate(PermissionCheck(action="web_research"))
        try:
            self.perm.authorize("agent_x", PermissionCheck(action="payment", amount_egp=99999))
        except ApprovalRequired:
            pass
        logs = self.repo.list_audit_logs()
        self.assertGreaterEqual(len(logs), 1)
        self.assertEqual(logs[0]["actor"], "agent_x")
        self.assertEqual(logs[0]["permission"], "PENDING_APPROVAL")

    def tearDown(self):
        self.db.close()


if __name__ == "__main__":
    unittest.main()
