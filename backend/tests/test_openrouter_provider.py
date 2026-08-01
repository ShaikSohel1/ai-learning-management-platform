"""
Test Suite: OpenRouter Provider Unit Tests.
Verifies OpenRouterProvider HTTPS requests, model-specific execution, and health check.
"""

import unittest
from unittest.mock import MagicMock, patch

from app.ai.providers.openrouter_provider import OpenRouterProvider


@patch("time.sleep", return_value=None)
class TestOpenRouterProvider(unittest.TestCase):
    def test_provider_name_and_models(self, mock_sleep):
        provider = OpenRouterProvider(api_key="mock_openrouter_key")
        self.assertEqual(provider.provider_name(), "OpenRouter")
        self.assertIn("openai/gpt-oss-20b", provider.get_available_models())

    @patch("httpx.Client.post")
    def test_generate_content_with_model_success(self, mock_post, mock_sleep):
        provider = OpenRouterProvider(api_key="mock_openrouter_key")

        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "choices": [{"message": {"content": "Hello from OpenRouter"}}]
        }
        mock_resp.raise_for_status.return_value = None
        mock_post.return_value = mock_resp

        res = provider.generate_content_with_model(
            model="openai/gpt-oss-20b",
            prompt="Test OpenRouter prompt"
        )
        self.assertEqual(res, "Hello from OpenRouter")

    @patch("httpx.Client.post")
    def test_json_mode(self, mock_post, mock_sleep):
        provider = OpenRouterProvider(api_key="mock_openrouter_key")

        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "choices": [{"message": {"content": '{"status": "ok", "provider": "OpenRouter"}'}}]
        }
        mock_resp.raise_for_status.return_value = None
        mock_post.return_value = mock_resp

        data = provider.generate_json_with_model(
            model="openai/gpt-oss-20b",
            prompt="Generate JSON"
        )
        self.assertEqual(data["status"], "ok")

    def test_health(self, mock_sleep):
        provider = OpenRouterProvider(api_key="mock_openrouter_key")
        h = provider.health()
        self.assertEqual(h["provider"], "OpenRouter")
        self.assertTrue(h["healthy"])
        self.assertIn("openai/gpt-oss-20b", h["available_models"])


if __name__ == "__main__":
    unittest.main()
