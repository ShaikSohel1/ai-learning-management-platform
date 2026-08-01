"""
AI Service Layer Package for AI Learning Management Platform.

Multi-Provider Multi-Model Architecture:
- llm_manager: Centralized LLMManager orchestrating Groq -> Gemini multi-model failover chains.
- provider_registry: Dynamic registry managing GroqProvider, GeminiProvider, OpenRouterProvider.
- prompt_manager: Versioned prompt templates & dynamic prompt builder.
- response_parser: JSON sanitization, parsing, and Pydantic validation.
- retry_handler: Exponential backoff for transient errors.
- conversation_memory: Multi-turn chat history management per user.
- ai_service: Unified business facade orchestrating AI workflows.
"""

from app.ai.ai_service import AIService, get_ai_service
from app.ai.llm_manager import LLMManager, get_llm_manager, llm_manager
from app.ai.provider_registry import ProviderRegistry, provider_registry
from app.ai.providers import AllProvidersExhaustedError, BaseProvider, ProviderUnavailableException

__all__ = [
    "AIService",
    "get_ai_service",
    "LLMManager",
    "get_llm_manager",
    "llm_manager",
    "ProviderRegistry",
    "provider_registry",
    "BaseProvider",
    "ProviderUnavailableException",
    "AllProvidersExhaustedError",
]
