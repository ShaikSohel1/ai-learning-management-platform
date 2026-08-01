"""
Base Provider Interface Module.

Defines the abstract base class and common exceptions for all LLM providers in the system.
Supports explicit model target execution for multi-provider multi-model failover chains.
"""

from abc import ABC, abstractmethod
import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


class ProviderUnavailableException(Exception):
    """Raised when all configured models/retries for an AI provider fail or the provider is unavailable."""

    def __init__(self, message: str | None = None) -> None:
        self.message = (
            message
            or "The selected AI provider is currently unavailable. Please try again shortly."
        )
        super().__init__(self.message)


class AllProvidersExhaustedError(ProviderUnavailableException):
    """Raised when every model from every configured AI provider in the system fails."""

    def __init__(self, message: str | None = None) -> None:
        self.message = (
            message
            or "All AI models and providers are currently unavailable. Please try again shortly."
        )
        super().__init__(self.message)


class BaseProvider(ABC):
    """
    Abstract Base Class for provider-agnostic AI model integrations.
    Supports model-specific execution for fine-grained multi-model failover chains.
    """

    @abstractmethod
    def generate_content_with_model(
        self,
        model: str,
        prompt: str,
        system_instruction: str | None = None,
        json_mode: bool = False
    ) -> str:
        """
        Generates text or JSON string using a specific model identifier.
        """
        pass

    @abstractmethod
    def generate_json_with_model(
        self,
        model: str,
        prompt: str,
        system_instruction: str | None = None
    ) -> dict[str, Any] | list[Any]:
        """
        Generates structured JSON object/list using a specific model identifier.
        """
        pass

    @abstractmethod
    def get_available_models(self) -> list[str]:
        """Returns ordered list of configured / discovered model identifiers for this provider."""
        pass

    @abstractmethod
    def provider_name(self) -> str:
        """Returns human-readable name of the AI provider (e.g. 'Groq', 'Gemini', 'OpenRouter')."""
        pass

    @abstractmethod
    def health(self) -> dict[str, Any]:
        """
        Returns real-time health diagnostic status of the provider.
        """
        pass

    def generate_content(
        self,
        prompt: str,
        system_instruction: str | None = None,
        json_mode: bool = False
    ) -> str:
        """Default generator executing against primary configured model."""
        models = self.get_available_models()
        target_model = models[0] if models else ""
        return self.generate_content_with_model(
            model=target_model,
            prompt=prompt,
            system_instruction=system_instruction,
            json_mode=json_mode
        )

    def generate_json(
        self,
        prompt: str,
        system_instruction: str | None = None
    ) -> dict[str, Any] | list[Any]:
        """Default JSON generator executing against primary configured model."""
        models = self.get_available_models()
        target_model = models[0] if models else ""
        return self.generate_json_with_model(
            model=target_model,
            prompt=prompt,
            system_instruction=system_instruction
        )

    def get_active_model(self) -> str:
        models = self.get_available_models()
        return models[0] if models else ""

    def _clean_json_markdown(self, raw_text: str) -> str:
        """Helper to trim ```json markdown wrappers if present in model output."""
        cleaned = raw_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:].strip()
        if cleaned.startswith("```"):
            cleaned = cleaned[3:].strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
        return cleaned
