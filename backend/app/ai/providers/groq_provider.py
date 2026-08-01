"""
Groq AI Provider Module.

Integrates official Groq SDK and REST API into the multi-provider multi-model architecture.
Supports configurable model chains:
GROQ_MODELS=llama-3.3-70b-versatile,deepseek-r1-distill-llama-70b,qwen/qwen3-32b,openai/gpt-oss-120b,llama-3.1-8b-instant
"""

import json
import logging
import time
from typing import Any

import httpx

from app.ai.providers.base_provider import BaseProvider, ProviderUnavailableException
from app.core.config import settings

logger = logging.getLogger("groq_provider")

try:
    from groq import Groq
    GROQ_SDK_AVAILABLE = True
except ImportError:
    Groq = None
    GROQ_SDK_AVAILABLE = False


class GroqProvider(BaseProvider):
    """Groq LLM Provider implementation for multi-model failover."""

    _active_model: str = ""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or settings.GROQ_API_KEY
        if self.api_key and GROQ_SDK_AVAILABLE:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as exc:
                logger.warning(f"Failed to initialize Groq SDK client: {exc}")
                self.client = None
        else:
            self.client = None

    @classmethod
    def set_active_model(cls, model_name: str) -> None:
        cls._active_model = model_name

    @classmethod
    def get_active_model_cls(cls) -> str:
        return cls._active_model or "llama-3.3-70b-versatile"

    def get_active_model(self) -> str:
        return GroqProvider.get_active_model_cls()


    def provider_name(self) -> str:
        return "Groq"

    def get_available_models(self) -> list[str]:
        return settings.GROQ_MODELS or [
            "llama-3.3-70b-versatile",
            "deepseek-r1-distill-llama-70b",
            "qwen/qwen3-32b",
            "openai/gpt-oss-120b",
            "llama-3.1-8b-instant"
        ]

    def generate_content_with_model(
        self,
        model: str,
        prompt: str,
        system_instruction: str | None = None,
        json_mode: bool = False
    ) -> str:
        if not self.api_key:
            logger.warning("No valid GROQ_API_KEY configured. Returning mock response.")
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
                return self._call_groq_api(
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

        raise RuntimeError(f"Groq model '{model}' failed after {max_retries} attempts. Error: {last_exception}")

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

    def _call_groq_api(
        self,
        model: str,
        messages: list[dict[str, str]],
        json_mode: bool,
        timeout: float
    ) -> str:
        if self.client:
            kwargs: dict[str, Any] = {
                "model": model,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 2048,
                "timeout": timeout,
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

            completion = self.client.chat.completions.create(**kwargs)
            if not completion.choices or not completion.choices[0].message.content:
                raise ValueError(f"Empty response from Groq model '{model}'")
            return completion.choices[0].message.content

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
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
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            choices = data.get("choices", [])
            if not choices or not choices[0].get("message", {}).get("content"):
                raise ValueError(f"Empty response from Groq HTTP API for model '{model}'")
            return choices[0]["message"]["content"]

    def health(self) -> dict[str, Any]:
        healthy = bool(self.api_key and self.api_key != "your_groq_api_key_here")
        models = self.get_available_models()
        return {
            "provider": self.provider_name(),
            "healthy": healthy,
            "available_models": models
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
                "summary": "Personalized learning path powered by Groq."
            }
            return json.dumps(fallback_obj)
        else:
            return "I am your AI Learning Assistant powered by Groq. How can I assist your career roadmap today?"
