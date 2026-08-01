"""
Test Suite: Groq Provider Unit Tests.
Verifies GroqProvider instantiation, model-specific content generation, JSON generation, and health metrics.
"""

import unittest
from unittest.mock import MagicMock, patch

from app.ai.providers.groq_provider import GroqProvider


@patch("time.sleep", return_value=None)
class TestGroqProvider(unittest.TestCase):
    def setUp(self):
        GroqProvider.set_active_model("llama-3.3-70b-versatile")

    def test_provider_name_and_models(self, mock_sleep):
        provider = GroqProvider(api_key="mock_groq_key")
        self.assertEqual(provider.provider_name(), "Groq")
        self.assertIn("llama-3.3-70b-versatile", provider.get_available_models())

    @patch("httpx.Client.post")
    def test_generate_content_with_model_success(self, mock_post, mock_sleep):
        provider = GroqProvider(api_key="mock_groq_key")
        provider.client = None

        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "choices": [{"message": {"content": "Hello from Groq Llama 3.3"}}]
        }
        mock_resp.raise_for_status.return_value = None
        mock_post.return_value = mock_resp

        res = provider.generate_content_with_model(
            model="llama-3.3-70b-versatile",
            prompt="Test prompt"
        )
        self.assertEqual(res, "Hello from Groq Llama 3.3")

    @patch("httpx.Client.post")
    def test_json_generation(self, mock_post, mock_sleep):
        provider = GroqProvider(api_key="mock_groq_key")
        provider.client = None

        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "choices": [{"message": {"content": '{"status": "success", "provider": "Groq"}'}}]
        }
        mock_resp.raise_for_status.return_value = None
        mock_post.return_value = mock_resp

        data = provider.generate_json_with_model(
            model="llama-3.3-70b-versatile",
            prompt="Generate JSON"
        )
        self.assertEqual(data["status"], "success")

    def test_health(self, mock_sleep):
        provider = GroqProvider(api_key="mock_groq_key")
        h = provider.health()
        self.assertEqual(h["provider"], "Groq")
        self.assertTrue(h["healthy"])
        self.assertIn("llama-3.3-70b-versatile", h["available_models"])


if __name__ == "__main__":
    unittest.main()
