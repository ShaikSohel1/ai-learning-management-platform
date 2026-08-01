"""
Test Suite: Gemini Provider Unit Tests.
Verifies GeminiProvider instantiation, model discovery, model-specific generation, and health check.
"""

import unittest
from unittest.mock import MagicMock, patch

from google.genai.errors import APIError

from app.ai.providers.gemini_provider import (
    AllGeminiModelsQuotaExhaustedError,
    GeminiProvider,
)
from app.ai.providers.base_provider import ProviderUnavailableException


def make_api_error(code: int, message: str) -> APIError:
    return APIError(code, {"error": {"message": message, "code": code}})


@patch("time.sleep", return_value=None)
class TestGeminiProvider(unittest.TestCase):
    def setUp(self):
        GeminiProvider.reset_active_model()

    def tearDown(self):
        GeminiProvider.reset_active_model()

    def test_provider_name_and_active_model(self, mock_sleep):
        provider = GeminiProvider(api_key="mock_key")
        self.assertEqual(provider.provider_name(), "Gemini")
        self.assertTrue(isinstance(provider.get_active_model(), str))

    def test_generate_content_with_model_success(self, mock_sleep):
        provider = GeminiProvider(api_key="mock_key")
        mock_genai_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"status": "ok"}'
        mock_genai_client.models.generate_content.return_value = mock_response
        provider.client = mock_genai_client

        output = provider.generate_content_with_model(
            model="models/gemini-3.5-flash",
            prompt="Test prompt"
        )
        self.assertEqual(output, '{"status": "ok"}')

    def test_generate_json_with_model(self, mock_sleep):
        provider = GeminiProvider(api_key="mock_key")
        mock_genai_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '```json\n{"result": "success"}\n```'
        mock_genai_client.models.generate_content.return_value = mock_response
        provider.client = mock_genai_client

        data = provider.generate_json_with_model(
            model="models/gemini-3.5-flash",
            prompt="JSON prompt"
        )
        self.assertEqual(data, {"result": "success"})

    def test_health_check(self, mock_sleep):
        provider = GeminiProvider(api_key="mock_key")
        h = provider.health()
        self.assertEqual(h["provider"], "Gemini")
        self.assertIn("healthy", h)
        self.assertIn("available_models", h)


if __name__ == "__main__":
    unittest.main()
