"""
Test Suite: Provider Failover & Resilience Integration Tests.
Verifies multi-provider multi-model failovers and AllProvidersExhaustedError raising.
"""

import unittest
from unittest.mock import MagicMock, patch

from app.ai.llm_manager import LLMManager
from app.ai.provider_registry import provider_registry
from app.ai.providers.base_provider import AllProvidersExhaustedError


@patch("time.sleep", return_value=None)
class TestProviderFailover(unittest.TestCase):
    def tearDown(self):
        provider_registry._register_default_providers()

    @patch("httpx.Client.post")
    def test_groq_failover_handling(self, mock_post, mock_sleep):
        pm = LLMManager(provider_name_override="groq")
        groq_p = pm.get_provider()
        groq_p.api_key = "mock_key"
        groq_p.client = None

        err_resp = MagicMock()
        err_resp.raise_for_status.side_effect = Exception("Groq Rate Limit")

        ok_resp = MagicMock()
        ok_resp.json.return_value = {
            "choices": [{"message": {"content": "Groq model fallback response"}}]
        }
        ok_resp.raise_for_status.return_value = None

        # Model 1 fails 3 times, Model 2 succeeds
        mock_post.side_effect = [err_resp, err_resp, err_resp, ok_resp]

        res = pm.generate_content("Testing Groq failover")
        self.assertEqual(res, "Groq model fallback response")

    @patch("httpx.Client.post")
    def test_provider_raises_all_providers_exhausted_exception(self, mock_post, mock_sleep):
        pm = LLMManager(provider_name_override="groq")
        groq_p = pm.get_provider()
        groq_p.api_key = "mock_key"
        groq_p.client = None

        gemini_p = provider_registry.get_provider("gemini")
        gemini_p.generate_content_with_model = MagicMock(side_effect=Exception("Gemini failed"))

        mock_post.side_effect = Exception("All Groq calls failed")

        with self.assertRaises(AllProvidersExhaustedError) as ctx:
            pm.generate_content("Exhaustion prompt")

        self.assertIn("failed", str(ctx.exception).lower())


if __name__ == "__main__":
    unittest.main()
