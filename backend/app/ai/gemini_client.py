"""
Gemini API Client Module with Production-Grade Model Failover System.

Encapsulates authentication, requests, telemetry logging, and automatic model failover
across configured Gemini model priorities using the official google-genai SDK.
"""

import json
import logging
import time
from typing import Any

from google import genai
from google.genai import types
from google.genai.errors import APIError

from app.core.config import settings

logger = logging.getLogger(__name__)

# Exact Priority Order Required by Platform Specifications
MODEL_PRIORITY_LIST: list[str] = [
    "models/gemini-2.5-flash",
    "models/gemini-3.6-flash",
    "models/gemini-3.5-flash",
    "models/gemini-3-flash",
    "models/gemini-3.5-flash-lite",
    "models/gemini-3.1-flash-lite",
    "models/gemini-2.5-flash-lite",
]

NON_RETRYABLE_STATUS_CODES = {400, 401, 403, 404}
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class AllGeminiModelsQuotaExhaustedError(Exception):
    """Raised when all configured Gemini models in the failover priority chain return 429 / quota exhausted."""

    def __init__(self, message: str | None = None):
        self.message = message or "All configured Gemini models have exhausted their available quota. Please try again later."
        super().__init__(self.message)


class GeminiClient:
    """Production-grade LLM client with intelligent active model caching and automatic quota failover."""

    # Class-level active model in-memory cache across requests (resets to primary on process restart)
    _active_model: str = MODEL_PRIORITY_LIST[0]

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None
    ) -> None:
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.preferred_model = model or settings.GEMINI_MODEL

        # Initialize official Google GenAI Client if a valid key is present
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    @classmethod
    def get_active_model(cls) -> str:
        """Returns currently active model string."""
        return cls._active_model

    @classmethod
    def set_active_model(cls, model_name: str) -> None:
        """Sets active model in-memory cache."""
        cls._active_model = cls._normalize_model_name(model_name)

    @classmethod
    def reset_active_model(cls) -> None:
        """Resets active model cache to preferred primary model."""
        cls._active_model = MODEL_PRIORITY_LIST[0]
        logger.info(f"Reset active Gemini model cache to primary: '{cls._active_model}'")

    @classmethod
    def _normalize_model_name(cls, model_name: str) -> str:
        if not model_name:
            return MODEL_PRIORITY_LIST[0]
        if not model_name.startswith("models/"):
            return f"models/{model_name}"
        return model_name

    @classmethod
    def _is_retryable_error(cls, exc: Exception) -> bool:
        """
        Determines whether an exception is retryable (429, 500, 503, 504, connection/timeouts)
        vs non-retryable (400, 401, 403, 404, invalid auth).
        """
        if isinstance(exc, (TimeoutError, ConnectionError)):
            return True

        if isinstance(exc, APIError):
            code = getattr(exc, "code", None)
            msg = str(exc).upper()

            if code in NON_RETRYABLE_STATUS_CODES:
                return False

            if code in RETRYABLE_STATUS_CODES:
                return True

            if any(term in msg for term in ("429", "RESOURCE_EXHAUSTED", "QUOTA", "RATE", "OVERLOADED", "500", "503")):
                return True

            if code is not None and code >= 500:
                return True

            return False

        if isinstance(exc, ValueError) and "empty" in str(exc).lower():
            return True

        return False

    @property
    def model(self) -> str:
        """Instance property returning current active model."""
        return GeminiClient._active_model

    def generate_content(
        self,
        prompt: str,
        system_instruction: str | None = None,
        json_mode: bool = True
    ) -> str:
        """
        Sends content generation request with automatic failover across priority models.

        Args:
            prompt: User prompt text.
            system_instruction: Optional system instructions.
            json_mode: Enforce JSON response format.

        Returns:
            Raw response text from Gemini model.
        """
        if not self.client:
            logger.warning("No valid GEMINI_API_KEY configured. Returning fallback mock response.")
            return self._generate_mock_fallback(prompt, json_mode)

        config = types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=2048,
        )
        if json_mode:
            config.response_mime_type = "application/json"
        if system_instruction:
            config.system_instruction = system_instruction

        # Determine attempt sequence starting from active_model
        current_active = GeminiClient._active_model
        try:
            start_idx = MODEL_PRIORITY_LIST.index(current_active)
        except ValueError:
            start_idx = 0

        ordered_models = MODEL_PRIORITY_LIST[start_idx:] + MODEL_PRIORITY_LIST[:start_idx]

        start_time = time.perf_counter()
        failovers = 0

        for candidate_model in ordered_models:
            logger.info(f"Using Gemini model: '{candidate_model}'")
            try:
                response = self.client.models.generate_content(
                    model=candidate_model,
                    contents=prompt,
                    config=config
                )

                if not response or not response.text:
                    logger.error(f"Gemini API returned an empty text response for model '{candidate_model}'.")
                    raise ValueError(f"Gemini API returned an empty response for model '{candidate_model}'.")

                latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

                # Update active model cache if failover occurred
                if candidate_model != GeminiClient._active_model:
                    logger.info(f"Switching active model to '{candidate_model}'")
                    GeminiClient._active_model = candidate_model

                logger.info(
                    f"Request succeeded on '{candidate_model}' "
                    f"(latency: {latency_ms}ms, failovers: {failovers})"
                )
                return response.text

            except Exception as exc:
                if not self._is_retryable_error(exc):
                    logger.error(f"Non-retryable client error on model '{candidate_model}': {exc}")
                    raise exc

                failovers += 1
                code_str = getattr(exc, "code", "429/Transient")
                logger.warning(
                    f"Quota/Transient error on '{candidate_model}' [Code {code_str}]: {exc}. "
                    f"Attempting failover to next model..."
                )

        logger.error(
            f"All {len(MODEL_PRIORITY_LIST)} configured Gemini models have exhausted their available quota or failed."
        )
        raise AllGeminiModelsQuotaExhaustedError(
            "All configured Gemini models have exhausted their available quota. Please try again later."
        )

    def _generate_mock_fallback(self, prompt: str, json_mode: bool) -> str:
        """
        Generates realistic fallback response when API key is unconfigured or in offline dev mode.
        """
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
                    },
                    {
                        "title": "PostgreSQL & Database Design Deep Dive",
                        "description": "Learn schema design, indexing strategies, complex query tuning, and ORM integration.",
                        "category": "Database Engineering",
                        "difficulty": "Intermediate",
                        "reason": "Crucial foundational skill for backend system architects."
                    },
                    {
                        "title": "Docker, Kubernetes & Microservices Deployment",
                        "description": "Containerize backend services, manage multi-container orchestration, and setup CI/CD pipelines.",
                        "category": "DevOps & Cloud",
                        "difficulty": "Advanced",
                        "reason": "Essential for scaling backend applications in production environments."
                    }
                ],
                "learning_path": [
                    {
                        "week": 1,
                        "topic": "Python Async Fundamentals & Data Structures",
                        "description": "Master advanced Python constructs, typing, asyncio, and clean code principles.",
                        "skills_to_acquire": ["Python 3.12+", "Asyncio", "Pydantic V2"]
                    },
                    {
                        "week": 2,
                        "topic": "FastAPI REST API Architecture & JWT Security",
                        "description": "Build high-performance REST APIs with dependency injection, OAuth2 JWT auth, and middleware.",
                        "skills_to_acquire": ["FastAPI", "JWT Auth", "REST Principles"]
                    },
                    {
                        "week": 3,
                        "topic": "Relational Databases & SQLAlchemy 2.0 ORM",
                        "description": "Design relational schemas, manage database migrations with Alembic, and optimize database queries.",
                        "skills_to_acquire": ["PostgreSQL", "SQLAlchemy", "Alembic"]
                    },
                    {
                        "week": 4,
                        "topic": "System Design, Microservices & Containerization",
                        "description": "Containerize services with Docker, handle message queues, and deploy robust cloud backends.",
                        "skills_to_acquire": ["Docker", "Redis", "Microservices Design"]
                    }
                ],
                "estimated_duration": "4 Weeks",
                "difficulty": "Intermediate",
                "summary": "This personalized learning path is tailored to bridge your existing technical background to a production-grade Backend Developer role. It focuses on modern async Python, database mastery, secure API architecture, and cloud deployment."
            }
            return json.dumps(fallback_obj)
        else:
            return "I am your AI Business Assistant. I can help you build custom learning paths, analyze skill gaps, recommend targeted courses, and provide career roadmap guidance!"
