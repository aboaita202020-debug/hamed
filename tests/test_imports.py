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
        import app.agents.opportunity_hunter_agent  # noqa: F401
        import app.agents.sales_agent  # noqa: F401
        import app.agents.negotiation_agent  # noqa: F401
        import app.agents.revenue_agent  # noqa: F401
        import app.agents.reporting_agent  # noqa: F401
        import app.agents.fact_check_agent  # noqa: F401

    def test_import_tools_and_db(self):
        from app.tools import ToolRegistry, WebSearchTool, CRMTool  # noqa: F401
        from app.db import Database, Repository  # noqa: F401
        from app.permissions import PermissionLayer  # noqa: F401


if __name__ == "__main__":
    unittest.main()
