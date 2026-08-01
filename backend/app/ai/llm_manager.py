"""
Centralized LLM Manager Module.

Orchestrates multi-provider multi-model failover execution:
Groq (Model 1 -> Model 2 -> Model 3 -> Model 4)
  ↓ (All Groq models failed)
Gemini (Model 1 -> Model 2 -> Model 3 -> Model 4 -> Model 5)
  ↓ (All Gemini models failed)
HTTP 503 Service Unavailable (AllProvidersExhaustedError)

Handles provider selection, model selection, retries, structured logging, latency metrics, and health status.
"""

import json
import logging
import time
from typing import Any

from app.ai.provider_registry import provider_registry
from app.ai.providers.base_provider import (
    AllProvidersExhaustedError,
    BaseProvider,
    ProviderUnavailableException,
)
from app.core.config import settings

logger = logging.getLogger("llm_manager")


class LLMManager:
    """
    Centralized Multi-Provider Multi-Model AI Orchestrator.
    Executes intra-provider multi-model chains before executing inter-provider failover.
    """

    def __init__(self, provider_name_override: str | None = None) -> None:
        self.primary_provider_name = (provider_name_override or settings.PRIMARY_PROVIDER).lower()
        self.fallback_provider_names = [p.lower() for p in settings.FALLBACK_PROVIDERS if p.lower() != self.primary_provider_name]
        
        self.last_successful_provider: str = self.primary_provider_name.capitalize()
        self.last_successful_model: str = ""
        self.current_provider: str = self.primary_provider_name.capitalize()
        self.current_model: str = ""

    def get_provider(self) -> BaseProvider | None:
        return provider_registry.get_provider(self.primary_provider_name)

    def set_provider(self, provider_name: str) -> None:
        self.primary_provider_name = provider_name.strip().lower()
        self.current_provider = self.primary_provider_name.capitalize()
        self.last_successful_provider = self.primary_provider_name.capitalize()



    def _get_provider_chain(self) -> list[str]:
        chain = [self.primary_provider_name]
        for p in self.fallback_provider_names:
            if p not in chain:
                chain.append(p)
        return chain

    def generate_content(
        self,
        prompt: str,
        system_instruction: str | None = None,
        json_mode: bool = False
    ) -> str:
        """
        Generates text or JSON response executing multi-provider multi-model failover loop.
        Groq Models -> Gemini Models -> AllProvidersExhaustedError (503).
        """
        provider_chain = self._get_provider_chain()
        attempted_logs: list[str] = []
        overall_start = time.perf_counter()

        for p_idx, provider_name in enumerate(provider_chain):
            provider_inst = provider_registry.get_provider(provider_name)
            if not provider_inst:
                logger.warning(f"Provider '{provider_name}' not found in registry. Skipping.")
                continue

            models = provider_inst.get_available_models()
            p_display_name = provider_inst.provider_name()

            if p_idx > 0:
                logger.info("==================================================")
                logger.info(f"Switching Provider")
                logger.info("↓")
                logger.info(f"{p_display_name}")
                logger.info("==================================================")

            for m_idx, model_candidate in enumerate(models):
                attempt_start = time.perf_counter()
                self.current_provider = p_display_name
                self.current_model = model_candidate

                try:
                    res_text = provider_inst.generate_content_with_model(
                        model=model_candidate,
                        prompt=prompt,
                        system_instruction=system_instruction,
                        json_mode=json_mode
                    )

                    if not res_text or not res_text.strip():
                        raise ValueError(f"Empty text response returned from model '{model_candidate}'")

                    latency_ms = round((time.perf_counter() - attempt_start) * 1000, 2)

                    self.last_successful_provider = p_display_name
                    self.last_successful_model = model_candidate

                    logger.info("==================================================")
                    logger.info(f"Provider : {p_display_name}")
                    logger.info(f"Model    : {model_candidate}")
                    logger.info(f"Attempt  : 1")
                    logger.info(f"Latency  : {latency_ms}ms")
                    logger.info(f"Status   : SUCCESS")
                    logger.info("==================================================")

                    return res_text

                except Exception as exc:
                    latency_ms = round((time.perf_counter() - attempt_start) * 1000, 2)
                    err_msg = str(exc)
                    attempted_logs.append(f"{p_display_name}:{model_candidate} ({err_msg[:60]})")

                    logger.warning("==================================================")
                    logger.warning(f"Provider : {p_display_name}")
                    logger.warning(f"Model    : {model_candidate}")
                    logger.warning(f"Latency  : {latency_ms}ms")
                    logger.warning(f"Status   : FAILED ({err_msg[:80]})")
                    logger.warning("==================================================")

                    if m_idx + 1 < len(models):
                        next_model = models[m_idx + 1]
                        logger.info(f"{p_display_name}")
                        logger.info("↓")
                        logger.info(f"{model_candidate} failed")
                        logger.info("↓")
                        logger.info(f"Switching Model")
                        logger.info("↓")
                        logger.info(f"{next_model}")

        total_time_ms = round((time.perf_counter() - overall_start) * 1000, 2)
        logger.error(
            f"All providers and models exhausted after {total_time_ms}ms. "
            f"Attempted: {', '.join(attempted_logs)}"
        )
        raise AllProvidersExhaustedError(
            "Every configured model across all AI providers failed. Please try again shortly."
        )

    def generate_json(
        self,
        prompt: str,
        system_instruction: str | None = None
    ) -> dict[str, Any] | list[Any]:
        raw_text = self.generate_content(
            prompt=prompt,
            system_instruction=system_instruction,
            json_mode=True
        )
        cleaned = self._clean_json_markdown(raw_text)
        return json.loads(cleaned)

    def _clean_json_markdown(self, raw_text: str) -> str:
        cleaned = raw_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:].strip()
        if cleaned.startswith("```"):
            cleaned = cleaned[3:].strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
        return cleaned

    def get_active_model(self) -> str:
        return self.last_successful_model or self.current_model or "llama-3.3-70b-versatile"

    def provider_name(self) -> str:
        return self.last_successful_provider or self.current_provider or "Groq"

    def health(self) -> dict[str, Any]:
        return self.get_health_status()

    def get_health_status(self) -> dict[str, Any]:
        groq_p = provider_registry.get_provider("groq")
        gemini_p = provider_registry.get_provider("gemini")

        groq_models = groq_p.get_available_models() if groq_p else []
        gemini_models = gemini_p.get_available_models() if gemini_p else []

        groq_health = groq_p.health().get("healthy", False) if groq_p else False
        gemini_health = gemini_p.health().get("healthy", False) if gemini_p else False

        overall_status = "Operational" if (groq_health or gemini_health) else "Degraded"

        return {
            "current_provider": self.provider_name(),
            "current_model": self.get_active_model(),
            "available_groq_models": groq_models,
            "available_gemini_models": gemini_models,
            "failover_status": overall_status,
            "last_successful_provider": self.last_successful_provider or "Groq",
            "last_successful_model": self.last_successful_model or (groq_models[0] if groq_models else "llama-3.3-70b-versatile"),
            "provider_health": {
                "Groq": "Healthy" if groq_health else "Degraded",
                "Gemini": "Healthy" if gemini_health else "Degraded"
            }
        }


# Global Singleton LLMManager Instance
llm_manager = LLMManager()


def get_llm_manager() -> LLMManager:
    """Dependency injection helper for FastAPI."""
    return llm_manager
