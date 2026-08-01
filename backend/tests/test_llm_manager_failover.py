"""
Test Suite: Centralized LLMManager Multi-Provider Multi-Model Failover.

Verifies:
1. Groq Model 1 success.
2. Groq Model 1 fail -> Groq Model 2 success.
3. Every Groq model fail -> Inter-provider failover -> Gemini Model 1 success.
4. Every Groq and Gemini model fail -> AllProvidersExhaustedError (HTTP 503).
5. GET /health/ai diagnostic metrics payload.
"""

import unittest
from unittest.mock import MagicMock, patch

from app.ai.llm_manager import LLMManager
from app.ai.provider_registry import provider_registry
from app.ai.providers.base_provider import (
    AllProvidersExhaustedError,
    BaseProvider,
)


class MockProvider(BaseProvider):
    def __init__(self, name: str, models: list[str]) -> None:
        self._name = name
        self._models = models
        self.fail_models: set[str] = set()
        self.mock_responses: dict[str, str] = {}

    def provider_name(self) -> str:
        return self._name

    def get_available_models(self) -> list[str]:
        return self._models

    def generate_content_with_model(
        self,
        model: str,
        prompt: str,
        system_instruction: str | None = None,
        json_mode: bool = False
    ) -> str:
        if model in self.fail_models:
            raise RuntimeError(f"Simulated failure for model '{model}'")
        return self.mock_responses.get(model, f"Response from {self._name}:{model}")

    def generate_json_with_model(
        self,
        model: str,
        prompt: str,
        system_instruction: str | None = None
    ) -> dict:
        return {"response": self.generate_content_with_model(model, prompt, system_instruction, True)}

    def health(self) -> dict:
        return {"provider": self._name, "healthy": True, "available_models": self._models}


@patch("time.sleep", return_value=None)
class TestLLMManagerFailover(unittest.TestCase):
    def setUp(self):
        self.groq_mock = MockProvider("Groq", ["groq-m1", "groq-m2", "groq-m3", "groq-m4"])
        self.gemini_mock = MockProvider("Gemini", ["gemini-m1", "gemini-m2", "gemini-m3", "gemini-m4", "gemini-m5"])

        provider_registry.register_provider("groq", self.groq_mock)
        provider_registry.register_provider("gemini", self.gemini_mock)

        self.manager = LLMManager()

    def tearDown(self):
        provider_registry._register_default_providers()


    def test_01_groq_primary_model_success(self, mock_sleep):
        res = self.manager.generate_content("Hello Groq Model 1")
        self.assertEqual(res, "Response from Groq:groq-m1")
        self.assertEqual(self.manager.last_successful_provider, "Groq")
        self.assertEqual(self.manager.last_successful_model, "groq-m1")

    def test_02_groq_model1_fails_model2_succeeds(self, mock_sleep):
        self.groq_mock.fail_models.add("groq-m1")

        res = self.manager.generate_content("Hello Groq Model 2")
        self.assertEqual(res, "Response from Groq:groq-m2")
        self.assertEqual(self.manager.last_successful_provider, "Groq")
        self.assertEqual(self.manager.last_successful_model, "groq-m2")

    def test_03_all_groq_models_fail_switch_to_gemini_model1(self, mock_sleep):
        self.groq_mock.fail_models = {"groq-m1", "groq-m2", "groq-m3", "groq-m4"}

        res = self.manager.generate_content("Hello Gemini Model 1")
        self.assertEqual(res, "Response from Gemini:gemini-m1")
        self.assertEqual(self.manager.last_successful_provider, "Gemini")
        self.assertEqual(self.manager.last_successful_model, "gemini-m1")

    def test_04_all_groq_and_all_gemini_models_fail_raises_exhausted_error(self, mock_sleep):
        self.groq_mock.fail_models = {"groq-m1", "groq-m2", "groq-m3", "groq-m4"}
        self.gemini_mock.fail_models = {"gemini-m1", "gemini-m2", "gemini-m3", "gemini-m4", "gemini-m5"}

        with self.assertRaises(AllProvidersExhaustedError):
            self.manager.generate_content("Exhaust all models")

    def test_05_health_payload_structure(self, mock_sleep):
        h = self.manager.get_health_status()
        self.assertIn("current_provider", h)
        self.assertIn("current_model", h)
        self.assertIn("available_groq_models", h)
        self.assertIn("available_gemini_models", h)
        self.assertIn("failover_status", h)
        self.assertIn("last_successful_provider", h)
        self.assertIn("last_successful_model", h)
        self.assertIn("provider_health", h)
        self.assertEqual(h["provider_health"]["Groq"], "Healthy")
        self.assertEqual(h["provider_health"]["Gemini"], "Healthy")


if __name__ == "__main__":
    unittest.main()
