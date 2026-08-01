"""
OpenRouter AI Provider Module.

Integrates OpenRouter API into the multi-provider multi-model architecture using HTTPS requests.
Endpoint      : https://openrouter.ai/api/v1/chat/completions
Primary Model : openai/gpt-oss-20b
Fallback Model: meta-llama/llama-3.1-70b-instruct
"""

import json
import logging
import time
from typing import Any

import httpx

from app.ai.providers.base_provider import BaseProvider, ProviderUnavailableException
from app.core.config import settings

logger = logging.getLogger("openrouter_provider")


class OpenRouterProvider(BaseProvider):
    """OpenRouter LLM Provider implementation via HTTPS REST API."""

    ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
    PRIMARY_MODEL = "openai/gpt-oss-20b"
    FALLBACK_MODEL = "meta-llama/llama-3.1-70b-instruct"

    _active_model: str = ""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or settings.OPENROUTER_API_KEY

    @classmethod
    def set_active_model(cls, model_name: str) -> None:
        cls._active_model = model_name

    @classmethod
    def get_active_model_cls(cls) -> str:
        return cls._active_model or cls.PRIMARY_MODEL

    def get_active_model(self) -> str:
        return OpenRouterProvider.get_active_model_cls()


    def provider_name(self) -> str:
        return "OpenRouter"

    def get_available_models(self) -> list[str]:
        return [self.PRIMARY_MODEL, self.FALLBACK_MODEL]

    def generate_content_with_model(
        self,
        model: str,
        prompt: str,
        system_instruction: str | None = None,
        json_mode: bool = False
    ) -> str:
        if not self.api_key:
            logger.warning("No valid OPENROUTER_API_KEY configured. Returning mock response.")
            return self._generate_mock_fallback(prompt, json_mode)

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        max_retries = max(1, settings.AI_MAX_RETRIES)
        backoff_factor = settings.AI_BACKOFF_FACTOR
        timeout = settings.AI_REQUEST_TIMEOUT

        delay = 1.0
        last_exception = None

        for attempt in range(1, max_retries + 1):
            try:
                return self._call_openrouter_api(
                    model=model,
                    messages=messages,
                    json_mode=json_mode,
                    timeout=timeout
                )
            except Exception as exc:
                last_exception = exc
                if attempt < max_retries:
                    time.sleep(delay)
                    delay *= backoff_factor

        raise RuntimeError(f"OpenRouter model '{model}' failed after {max_retries} attempts. Error: {last_exception}")

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

    def _call_openrouter_api(
        self,
        model: str,
        messages: list[dict[str, str]],
        json_mode: bool,
        timeout: float
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-learning-platform.internal",
            "X-Title": "AI Learning Management Platform",
        }
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 2048,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        with httpx.Client(timeout=timeout) as client:
            resp = client.post(
                self.ENDPOINT,
                headers=headers,
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            choices = data.get("choices", [])
            if not choices or not choices[0].get("message", {}).get("content"):
                raise ValueError(f"Empty response from OpenRouter API for model '{model}'")
            return choices[0]["message"]["content"]

    def health(self) -> dict[str, Any]:
        healthy = bool(self.api_key and self.api_key != "your_openrouter_api_key_here")
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
                "summary": "Personalized learning path powered by OpenRouter."
            }
            return json.dumps(fallback_obj)
        else:
            return "I am your AI Learning Assistant powered by OpenRouter. How can I assist your career roadmap today?"
