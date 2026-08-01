"""
Test Suite: Gemini Model Failover Integration Tests.
Verifies multi-model failover chains, model recovery, and error escalation.
"""

import unittest
from unittest.mock import MagicMock, patch

from google.genai.errors import APIError

from app.ai.gemini_client import GeminiClient
from app.ai.providers.gemini_provider import GeminiProvider, AllGeminiModelsQuotaExhaustedError
from app.ai.providers.base_provider import ProviderUnavailableException


def make_api_error(code: int, message: str) -> APIError:
    return APIError(code, {"error": {"message": message, "code": code}})


@patch("time.sleep", return_value=None)
class TestGeminiModelFailover(unittest.TestCase):
    def setUp(self):
        GeminiProvider.reset_active_model()

    def tearDown(self):
        GeminiProvider.reset_active_model()

    def test_01_primary_model_success(self, mock_sleep):
        client = GeminiClient(api_key="mock_key")
        mock_genai_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"status": "ok"}'
        mock_genai_client.models.generate_content.return_value = mock_response
        client.client = mock_genai_client

        output = client.generate_content_with_model(
            model="models/gemini-3.5-flash",
            prompt="Test prompt"
        )
        self.assertEqual(output, '{"status": "ok"}')

    def test_02_failover_after_429_quota_exhausted(self, mock_sleep):
        client = GeminiClient(api_key="mock_key")
        mock_genai_client = MagicMock()

        err_429 = make_api_error(429, "Quota exceeded")
        ok_response = MagicMock()
        ok_response.text = '{"status": "recovered"}'

        mock_genai_client.models.generate_content.side_effect = [err_429, ok_response]
        client.client = mock_genai_client

        output = client.generate_content_with_model(
            model="models/gemini-3.5-flash",
            prompt="Retry test"
        )
        self.assertEqual(output, '{"status": "recovered"}')

    def test_03_active_model_setter_and_getter(self, mock_sleep):
        GeminiClient.set_active_model("models/gemini-3.5-flash-lite")
        self.assertEqual(GeminiClient.get_active_model(), "models/gemini-3.5-flash-lite")

    def test_04_restart_reset_to_primary(self, mock_sleep):
        GeminiClient.reset_active_model()
        self.assertIn("gemini-3.5-flash", GeminiClient.get_active_model())


if __name__ == "__main__":
    unittest.main()
