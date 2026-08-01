"""
Google Gemini AI Provider Module.

Integrates official google-genai SDK into the multi-provider multi-model architecture.
Preserves dynamic model discovery, self-healing runtime registry, per-model retries,
and model-specific execution for fine-grained failover chains.
"""

import json
import logging
import time
from typing import Any

from google import genai
from google.genai import types

from app.ai.providers.base_provider import BaseProvider, ProviderUnavailableException
from app.core.config import settings

logger = logging.getLogger("gemini_provider")


class AllGeminiModelsQuotaExhaustedError(ProviderUnavailableException):
    """Raised when all configured Gemini models fail."""

    def __init__(self, message: str | None = None):
        self.message = (
            message
            or "All configured Gemini models are currently unavailable. Please try again shortly."
        )
        super().__init__(self.message)


class GeminiProvider(BaseProvider):

    """Production-grade Google Gemini AI Provider."""

    _active_model: str = ""
    _discovered_models: list[str] = []
    _last_discovery_timestamp: float = 0.0

    PREFERRED_MODEL_ORDER: list[str] = [
        "models/gemini-3.6-flash",
        "models/gemini-3.5-flash",
        "models/gemini-flash-latest",
        "models/gemini-3.5-flash-lite",
        "models/gemini-3.1-flash-lite"
    ]

    def __init__(
        self,
        api_key: str | None = None
    ) -> None:
        self.api_key = api_key or settings.GEMINI_API_KEY
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as exc:
                logger.warning(f"Failed to initialize Gemini Client: {exc}")
                self.client = None
        else:
            self.client = None

        self.discover_available_models()

    @classmethod
    def get_active_model(cls) -> str:
        if not cls._active_model or "gemini-2.5-flash" in cls._active_model:
            cls._active_model = "models/gemini-3.5-flash"
        return cls._active_model

    @classmethod
    def set_active_model(cls, model_name: str) -> None:
        cls._active_model = model_name

    @classmethod
    def reset_active_model(cls) -> None:
        cls._active_model = "models/gemini-3.5-flash"


    def provider_name(self) -> str:
        return "Gemini"

    def get_available_models(self) -> list[str]:
        discovered = self.discover_available_models()
        configured = settings.GEMINI_MODELS
        
        chain = []
        for m in configured:
            norm = self._normalize_model_name(m)
            if norm not in chain:
                chain.append(norm)
        for m in discovered:
            norm = self._normalize_model_name(m)
            if norm not in chain:
                chain.append(norm)

        return chain or [
            "models/gemini-3.6-flash",
            "models/gemini-3.5-flash",
            "models/gemini-flash-latest",
            "models/gemini-3.5-flash-lite",
            "models/gemini-3.1-flash-lite"
        ]

    def _normalize_model_name(self, model_name: str) -> str:
        if not model_name:
            return "models/gemini-3.5-flash"
        cleaned = model_name.strip()
        if not cleaned.startswith("models/"):
            return f"models/{cleaned}"
        return cleaned

    def discover_available_models(self, force: bool = False) -> list[str]:
        now = time.time()
        if not force and GeminiProvider._discovered_models and (now - GeminiProvider._last_discovery_timestamp < 3600):
            return GeminiProvider._discovered_models

        if not self.client:
            GeminiProvider._discovered_models = settings.GEMINI_MODELS
            return GeminiProvider._discovered_models

        discovered: list[str] = []
        try:
            sdk_models = list(self.client.models.list())
            for m in sdk_models:
                m_name = m.name if hasattr(m, "name") else str(m)
                if "gemini-2.5-flash" in m_name and "lite" not in m_name and "preview" not in m_name:
                    continue
                discovered.append(self._normalize_model_name(m_name))

            logger.info(f"[Gemini Model Discovery] Total models listed: {len(sdk_models)}")
        except Exception as exc:
            logger.warning(f"[Gemini Model Discovery] Failed to list models via SDK: {exc}")

        chain = []
        for m in settings.GEMINI_MODELS:
            norm = self._normalize_model_name(m)
            if norm not in chain:
                chain.append(norm)
        for d in discovered:
            if d not in chain and "embedding" not in d and "imagen" not in d and "veo" not in d:
                chain.append(d)

        chain = [m for m in chain if m != "models/gemini-2.5-flash"]
        GeminiProvider._discovered_models = chain
        GeminiProvider._last_discovery_timestamp = now
        return chain

    def generate_content_with_model(
        self,
        model: str,
        prompt: str,
        system_instruction: str | None = None,
        json_mode: bool = False
    ) -> str:
        if not self.client:
            logger.warning("No valid GEMINI_API_KEY configured. Returning mock response.")
            return self._generate_mock_fallback(prompt, json_mode)

        norm_model = self._normalize_model_name(model)

        config = types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=2048,
            top_p=1.0,
            top_k=40,
        )
        if json_mode:
            config.response_mime_type = "application/json"
        if system_instruction:
            config.system_instruction = system_instruction

        max_retries = max(1, settings.AI_MAX_RETRIES)
        backoff_factor = settings.AI_BACKOFF_FACTOR

        delay = 1.0
        last_exception = None

        for attempt in range(1, max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=norm_model,
                    contents=prompt,
                    config=config
                )
                if not response or not response.text:
                    raise ValueError(f"Empty text response from Gemini model '{norm_model}'")
                return response.text
            except Exception as exc:
                last_exception = exc
                if attempt < max_retries:
                    time.sleep(delay)
                    delay *= backoff_factor

        raise RuntimeError(f"Gemini model '{norm_model}' failed after {max_retries} attempts. Error: {last_exception}")

    def generate_json_with_model(
        self,
        model: str,
        prompt: str,
        system_instruction: str | None = None
    ) -> dict[str, Any] | list[Any]:
        raw_text = self.generate_content_with_model(
            model=model,
            prompt=prompt,
            system_instruction=system_instruction,
            json_mode=True
        )
        cleaned = self._clean_json_markdown(raw_text)
        return json.loads(cleaned)

    def health(self) -> dict[str, Any]:
        healthy = bool(self.client and settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here")
        return {
            "provider": self.provider_name(),
            "healthy": healthy,
            "available_models": self.get_available_models()
        }

    def _generate_mock_fallback(self, prompt: str, json_mode: bool) -> str:
        if json_mode and ("learning_path" in prompt.lower() or "career_goal" in prompt.lower()):
            fallback_obj = {
                "career_goal": "Backend Developer",
                "recommended_courses": [
                    {
                        "title": "Mastering Python & FastAPI Architecture",
                        "description": "Comprehensive guide to building async microservices with Python, FastAPI, and SQLAlchemy.",
                        "category": "Backend Development",
                        "difficulty": "Intermediate",
                        "reason": "Directly aligns with modern cloud-native backend development requirements."
                    }
                ],
                "learning_path": [
                    {
                        "week": 1,
                        "topic": "Python Async Fundamentals & Data Structures",
                        "description": "Master advanced Python constructs, typing, asyncio, and clean code principles.",
                        "skills_to_acquire": ["Python 3.12+", "Asyncio", "Pydantic V2"]
                    }
                ],
                "estimated_duration": "4 Weeks",
                "difficulty": "Intermediate",
                "summary": "Personalized learning path powered by Gemini."
            }
            return json.dumps(fallback_obj)
        else:
            return "I am your AI Learning Assistant powered by Gemini. How can I assist your career roadmap today?"
