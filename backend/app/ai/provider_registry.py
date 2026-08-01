"""
Provider Registry Module.

Centralized registry managing provider instances (Groq, Gemini, OpenRouter, etc.).
Allows dynamic provider registration, lookup, and enumeration.
"""

import logging

from app.ai.providers.base_provider import BaseProvider
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.providers.groq_provider import GroqProvider
from app.ai.providers.openrouter_provider import OpenRouterProvider

logger = logging.getLogger("provider_registry")


class ProviderRegistry:
    """Registry maintaining active provider singleton instances."""

    def __init__(self) -> None:
        self._providers: dict[str, BaseProvider] = {}
        self._register_default_providers()

    def _register_default_providers(self) -> None:
        self._providers["groq"] = GroqProvider()
        self._providers["gemini"] = GeminiProvider()
        self._providers["openrouter"] = OpenRouterProvider()
        logger.info(f"ProviderRegistry initialized with providers: {list(self._providers.keys())}")

    def register_provider(self, name: str, provider: BaseProvider) -> None:
        clean_name = name.strip().lower()
        self._providers[clean_name] = provider
        logger.info(f"Registered new provider '{clean_name}' in ProviderRegistry")

    def get_provider(self, name: str) -> BaseProvider | None:
        clean_name = name.strip().lower()
        return self._providers.get(clean_name)

    def get_registered_provider_names(self) -> list[str]:
        return list(self._providers.keys())

    def get_all_providers(self) -> dict[str, BaseProvider]:
        return dict(self._providers)


# Global Singleton Instance
provider_registry = ProviderRegistry()
