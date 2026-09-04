import unittest

from app.ai_providers import AIProviderRouter, BaseAIProvider, AIResponse


class FailingProvider(BaseAIProvider):
    name = "failing"

    def is_configured(self):
        return True

    def complete(self, prompt, system=None):
        return AIResponse(success=False, provider=self.name, error="simulated_outage")


class WorkingProvider(BaseAIProvider):
    name = "working"

    def is_configured(self):
        return True

    def complete(self, prompt, system=None):
        return AIResponse(success=True, provider=self.name, text=f"echo: {prompt}",
                           cost_estimate_usd=0.001)


class UnconfiguredProvider(BaseAIProvider):
    name = "unconfigured"

    def is_configured(self):
        return False

    def complete(self, prompt, system=None):  # pragma: no cover
        raise AssertionError("should never be called when unconfigured")


class TestAIProviderRouter(unittest.TestCase):
    def test_falls_back_to_working_provider(self):
        router = AIProviderRouter(default_provider="failing")
        router.register(FailingProvider())
        router.register(WorkingProvider())
        router.register(UnconfiguredProvider())

        response = router.complete("hello")
        self.assertTrue(response.success)
        self.assertEqual(response.provider, "working")
        self.assertGreater(router.total_cost_usd, 0)

    def test_no_provider_configured_reports_clear_error(self):
        router = AIProviderRouter(default_provider="ghost")
        response = router.complete("hello")
        self.assertFalse(response.success)
        self.assertEqual(response.error, "no_ai_provider_configured")


if __name__ == "__main__":
    unittest.main()
