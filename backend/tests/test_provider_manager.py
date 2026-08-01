"""
Test Suite: AI Provider Manager Unit Tests.
Verifies LLMManager provider selection, unified delegation, and health status reporting.
"""

import unittest
from unittest.mock import MagicMock, patch

from app.ai.llm_manager import LLMManager
from app.ai.provider_registry import provider_registry
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.providers.groq_provider import GroqProvider
from app.ai.providers.openrouter_provider import OpenRouterProvider


@patch("time.sleep", return_value=None)
class TestAIProviderManager(unittest.TestCase):
    def test_instantiate_groq_by_default(self, mock_sleep):
        pm = LLMManager(provider_name_override="groq")
        self.assertEqual(pm.provider_name(), "Groq")
        self.assertTrue(isinstance(pm.get_provider(), GroqProvider))

    def test_instantiate_gemini(self, mock_sleep):
        pm = LLMManager(provider_name_override="gemini")
        self.assertEqual(pm.primary_provider_name, "gemini")
        self.assertTrue(isinstance(pm.get_provider(), GeminiProvider))

    def test_instantiate_openrouter(self, mock_sleep):
        pm = LLMManager(provider_name_override="openrouter")
        self.assertEqual(pm.primary_provider_name, "openrouter")
        self.assertTrue(isinstance(pm.get_provider(), OpenRouterProvider))

    def test_dynamic_provider_switching(self, mock_sleep):
        pm = LLMManager(provider_name_override="gemini")
        self.assertEqual(pm.primary_provider_name, "gemini")

        pm.set_provider("groq")
        self.assertEqual(pm.primary_provider_name, "groq")

    def test_unified_health_delegation(self, mock_sleep):
        pm = LLMManager(provider_name_override="groq")
        h = pm.health()
        self.assertIn("current_provider", h)
        self.assertIn("current_model", h)
        self.assertIn("available_groq_models", h)
        self.assertIn("available_gemini_models", h)
        self.assertIn("provider_health", h)


if __name__ == "__main__":
    unittest.main()
