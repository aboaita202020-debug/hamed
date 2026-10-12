"""
Regression test for the exact bug reported in the spec (section 22):
    ImportError: cannot import name 'HamedOrchestrator' from app.agents.orchestrator
"""
import unittest


class TestImports(unittest.TestCase):
    def test_import_from_orchestrator_module(self):
        from app.agents.orchestrator import HamedOrchestrator
        self.assertTrue(callable(HamedOrchestrator))

    def test_import_from_agents_package(self):
        from app.agents import HamedOrchestrator
        self.assertTrue(callable(HamedOrchestrator))

    def test_import_config(self):
        from app.config import settings
        self.assertIsNotNone(settings)

    def test_import_all_agent_modules(self):
        import app.agents.opportunity_hunter_agent as opp_agent
        import app.agents.sales_agent as sales_agent
        import app.agents.negotiation_agent as neg_agent
        import app.agents.revenue_agent as rev_agent
        import app.agents.reporting_agent as report_agent
        import app.agents.fact_check_agent as fact_agent
        for module in (opp_agent, sales_agent, neg_agent, rev_agent, report_agent, fact_agent):
            self.assertIsNotNone(module)

    def test_import_tools_and_db(self):
        from app.tools import ToolRegistry, WebSearchTool, CRMTool
        from app.db import Database, Repository
        from app.permissions import PermissionLayer
        for obj in (ToolRegistry, WebSearchTool, CRMTool, Database, Repository, PermissionLayer):
            self.assertIsNotNone(obj)


if __name__ == "__main__":
    unittest.main()
