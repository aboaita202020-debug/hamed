import os
import unittest

from app.free_ai_scout import candidates, discover


class TestFreeAIScout(unittest.TestCase):
    def test_catalog_contains_freellmapi(self):
        ids = {x["id"] for x in candidates()}
        self.assertIn("freellmapi", ids)

    def test_discovery_never_returns_secret_values(self):
        os.environ["FREELLMAPI_API_KEY"] = "DO_NOT_RETURN"
        rows = discover()
        self.assertTrue(any(x["id"] == "freellmapi" for x in rows))
        self.assertNotIn("DO_NOT_RETURN", str(rows))
        os.environ.pop("FREELLMAPI_API_KEY", None)


if __name__ == "__main__":
    unittest.main()
