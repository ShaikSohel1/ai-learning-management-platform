"""
Centralized Gemini Model Manager with Dynamic Self-Healing Runtime Model Registry.

Discovers available Gemini generation models dynamically via the official google-genai SDK,
maintains an in-memory runtime model registry, executes automatic multi-model failovers,
and logs structured execution telemetry.
"""

import json
import logging
import time
from typing import Any

from google import genai
from google.genai import types
from google.genai.errors import APIError

from app.core.config import settings

logger = logging.getLogger("gemini_client")


class AllGeminiModelsQuotaExhaustedError(Exception):
    """Raised when all configured Gemini models in the failover chain fail."""

    def __init__(self, message: str | None = None):
        self.message = (
            message
            or "All configured Gemini models are currently unavailable. Please try again shortly."
        )
        super().__init__(self.message)


class GeminiClient:
    """
    Centralized production-grade Gemini LLM Model Manager.
    Handles dynamic model discovery, per-model retries, automatic failover across models,
    and active model telemetry.
    """

    # Class-level active model tracking & discovered registry cache across requests
    _active_model: str = ""
    _discovered_models: list[str] = []
    _last_discovery_timestamp: float = 0.0

    PREFERRED_MODEL_ORDER: list[str] = [
        "models/gemini-3.6-flash",
        "models/gemini-3.5-flash",
        "models/gemini-flash-latest",
        "models/gemini-pro-latest",
        "models/gemini-3.5-flash-lite",
        "models/gemini-3.1-flash-lite",
        "models/gemini-2.0-flash",
        "models/gemini-1.5-flash",
        "models/gemini-1.5-pro",
    ]

    def __init__(
        self,
        api_key: str | None = None,
        preferred_model: str | None = None
    ) -> None:
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.preferred_model = self._normalize_model_name(
            preferred_model or settings.PRIMARY_GEMINI_MODEL
        )

        if self.api_key and self.api_key != "your_gemini_api_key_here":
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

        # Discover available models on initial load or if cache expired (1 hour TTL)
        self.discover_available_models()

        if not GeminiClient._active_model or "gemini-2.5-flash" in GeminiClient._active_model:
            model_chain = self.get_model_chain()
            GeminiClient._active_model = model_chain[0] if model_chain else self.preferred_model

    @classmethod
    def get_active_model(cls) -> str:
        """Returns currently active Gemini model name."""
        if not cls._active_model or "gemini-2.5-flash" in cls._active_model:
            cls._active_model = "models/gemini-3.5-flash"
        return cls._active_model

    @classmethod
    def set_active_model(cls, model_name: str) -> None:
        """Sets active Gemini model in memory."""
        cls._active_model = cls._normalize_model_name(model_name)

    @classmethod
    def get_discovered_models(cls) -> list[str]:
        """Returns runtime discovered available models."""
        return cls._discovered_models or cls.PREFERRED_MODEL_ORDER

    @classmethod
    def reset_active_model(cls) -> None:
        """Resets active model cache to primary preferred model."""
        cls._active_model = cls._normalize_model_name(settings.PRIMARY_GEMINI_MODEL)
        logger.info(f"Reset active Gemini model cache to primary: '{cls._active_model}'")

    @classmethod
    def _normalize_model_name(cls, model_name: str) -> str:
        """Ensures model name is cleanly formatted with models/ prefix."""
        if not model_name:
            return "models/gemini-3.5-flash"
        cleaned = model_name.strip()
        if not cleaned.startswith("models/"):
            return f"models/{cleaned}"
        return cleaned

    def discover_available_models(self, force: bool = False) -> list[str]:
        """
        STEP 5 & STEP 6: Real Model Discovery & Self-Healing Registry.
        Queries Gemini SDK for models available for current API key, filters out unavailable/deprecated models,
        and updates runtime available model registry.
        """
        now = time.time()
        if not force and GeminiClient._discovered_models and (now - GeminiClient._last_discovery_timestamp < 3600):
            return GeminiClient._discovered_models

        if not self.client:
            GeminiClient._discovered_models = GeminiClient.PREFERRED_MODEL_ORDER
            return GeminiClient._discovered_models

        discovered: list[str] = []
        try:
            sdk_models = list(self.client.models.list())
            for m in sdk_models:
                m_name = m.name if hasattr(m, "name") else str(m)
                # Exclude explicitly deprecated / unavailable models
                if "gemini-2.5-flash" in m_name and "lite" not in m_name and "preview" not in m_name:
                    continue
                discovered.append(self._normalize_model_name(m_name))

            logger.info(f"[Model Discovery] Total Gemini SDK models listed: {len(sdk_models)}")
        except Exception as exc:
            logger.warning(f"[Model Discovery] Failed to list models via SDK: {exc}")

        # Build prioritized chain matching discovered models
        ordered_chain: list[str] = []
        for pref in GeminiClient.PREFERRED_MODEL_ORDER:
            if pref not in ordered_chain and (not discovered or pref in discovered or "3.5" in pref or "3.6" in pref or "latest" in pref):
                ordered_chain.append(pref)

        # Append any remaining discovered models not in preferred list
        for d in discovered:
            if d not in ordered_chain and "embedding" not in d and "imagen" not in d and "veo" not in d:
                ordered_chain.append(d)

        # Clean out gemini-2.5-flash exact matches
        ordered_chain = [m for m in ordered_chain if m != "models/gemini-2.5-flash"]

        GeminiClient._discovered_models = ordered_chain
        GeminiClient._last_discovery_timestamp = now
        logger.info(f"[Model Discovery] Self-Healing Registry Initialized ({len(ordered_chain)} models available). First preference: '{ordered_chain[0]}'")
        return ordered_chain

    def get_model_chain(self) -> list[str]:
        """
        Constructs the prioritized model chain starting from active model,
        followed by runtime discovered/configured fallback models without duplicates.
        """
        discovered = self.discover_available_models()
        primary = self._normalize_model_name(settings.PRIMARY_GEMINI_MODEL)

        chain = []
        if primary != "models/gemini-2.5-flash" and primary not in chain:
            chain.append(primary)

        for m in discovered:
            if m not in chain and m != "models/gemini-2.5-flash":
                chain.append(m)

        for m in settings.FALLBACK_GEMINI_MODELS:
            norm_m = self._normalize_model_name(m)
            if norm_m not in chain and norm_m != "models/gemini-2.5-flash":
                chain.append(norm_m)

        # Fallback safety default
        if not chain:
            chain = [
                "models/gemini-3.5-flash",
                "models/gemini-3.6-flash",
                "models/gemini-flash-latest",
                "models/gemini-pro-latest",
                "models/gemini-2.0-flash",
            ]
        return chain

    @property
    def model(self) -> str:
        """Instance property returning current active model."""
        return GeminiClient.get_active_model()

    def generate_content(
        self,
        prompt: str,
        system_instruction: str | None = None,
        json_mode: bool = True
    ) -> str:
        """
        Generates text or JSON content using centralized multi-model failover.
        Retries transient errors per model, and automatically fails over across models on failure.
        """
        if not self.client:
            logger.warning("No valid GEMINI_API_KEY configured. Returning mock fallback response.")
            return self._generate_mock_fallback(prompt, json_mode)

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

        model_chain = self.get_model_chain()

        # Re-order chain so current active_model is tried first if valid
        active_curr = GeminiClient.get_active_model()
        if active_curr in model_chain:
            idx = model_chain.index(active_curr)
            model_chain = model_chain[idx:] + model_chain[:idx]

        max_retries = max(1, settings.GEMINI_MAX_RETRIES)
        backoff_factor = settings.GEMINI_BACKOFF_FACTOR

        overall_start_time = time.perf_counter()
        failover_count = 0
        attempted_errors: list[str] = []

        total_candidates = len(model_chain)
        logger.info(f"================================================")
        logger.info(f"Primary model: {model_chain[0]}")

        for idx, model_candidate in enumerate(model_chain):
            logger.info("================================================")
            logger.info(f"Trying model: {model_candidate}")
            logger.info("================================================")
            delay = 1.0

            for attempt in range(1, max_retries + 1):
                try:
                    response = self.client.models.generate_content(
                        model=model_candidate,
                        contents=prompt,
                        config=config
                    )

                    if not response or not response.text:
                        raise ValueError(f"Empty text response from model '{model_candidate}'")

                    latency_ms = round((time.perf_counter() - overall_start_time) * 1000, 2)

                    # Update active model cache if failover occurred
                    if model_candidate != GeminiClient._active_model:
                        GeminiClient.set_active_model(model_candidate)

                    logger.info("================================================")
                    logger.info("SUCCESS")
                    logger.info(f"Current model: {model_candidate}")
                    logger.info(f"Latency: {latency_ms}ms (Failovers: {failover_count}, Attempt: {attempt})")
                    logger.info("================================================")
                    return response.text

                except Exception as exc:
                    err_msg = str(exc)
                    status_code = getattr(exc, "code", None) or getattr(exc, "status_code", "404/Error")
                    is_not_found = "404" in err_msg or "NOT_FOUND" in err_msg or status_code == 404
                    is_deprecated = "no longer available" in err_msg.lower() or "deprecated" in err_msg.lower() or "not found" in err_msg.lower()

                    logger.warning("================================================")
                    logger.warning("FAILED")
                    logger.warning(f"HTTP STATUS: {status_code}")
                    logger.warning(f"Exception: {exc}")
                    logger.warning("================================================")

                    # 404 / Deprecated / Unavailable -> Skip remaining retries for THIS model and failover immediately
                    if is_not_found or is_deprecated:
                        attempted_errors.append(f"{model_candidate} ({status_code})")
                        if idx + 1 < total_candidates:
                            next_model = model_chain[idx + 1]
                            logger.info("================================================")
                            logger.info(f"Switching to: {next_model}")
                            logger.info("================================================")
                        break

                    # If not last attempt for this model, exponential backoff retry
                    if attempt < max_retries:
                        logger.info(f"Retrying model '{model_candidate}' in {delay:.2f}s (Attempt {attempt + 1}/{max_retries})...")
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        attempted_errors.append(f"{model_candidate} ({err_msg[:60]})")
                        if idx + 1 < total_candidates:
                            next_model = model_chain[idx + 1]
                            logger.info("================================================")
                            logger.info(f"Switching to: {next_model}")
                            logger.info("================================================")

            failover_count += 1

        # All models in chain exhausted
        total_time_ms = round((time.perf_counter() - overall_start_time) * 1000, 2)
        logger.error(
            f"All {len(model_chain)} Gemini models in failover chain exhausted after {total_time_ms}ms. "
            f"Errors: {', '.join(attempted_errors)}"
        )
        raise AllGeminiModelsQuotaExhaustedError(
            "All configured Gemini models are currently unavailable. Please try again shortly."
        )

    def _generate_mock_fallback(self, prompt: str, json_mode: bool) -> str:
        """
        Generates realistic fallback response when GEMINI_API_KEY is unconfigured or in dev mode.
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
                    }
                ],
                "estimated_duration": "4 Weeks",
                "difficulty": "Intermediate",
                "summary": "This personalized learning path is tailored to bridge your existing technical background to a production-grade Backend Developer role."
            }
            return json.dumps(fallback_obj)
        else:
            return "I am your AI Learning Assistant. How can I assist your career roadmap, course recommendations, or technical learning goals today?"


# Centralized helper function for standard call sites
def generate_with_fallback(
    prompt: str,
    system_instruction: str | None = None,
    json_mode: bool = True
) -> str:
    """
    Centralized wrapper function for executing Gemini API calls with automatic multi-model failover.
    """
    client = GeminiClient()
    return client.generate_content(
        prompt=prompt,
        system_instruction=system_instruction,
        json_mode=json_mode
    )
