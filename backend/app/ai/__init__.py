"""
AI Service Layer Package for AI Learning Management Platform.

Provides a modular architecture wrapping Google Gemini API:
- gemini_client: Low-level API caller & SDK/REST connection manager.
- prompt_manager: Versioned prompt templates & dynamic prompt builder.
- response_parser: JSON sanitization, parsing, and Pydantic validation.
- retry_handler: Exponential backoff for transient errors (429, 500, timeouts).
- conversation_memory: Multi-turn chat history management per user.
- ai_service: Unified business facade orchestrating the AI workflow.
"""

from app.ai.ai_service import AIService, get_ai_service

__all__ = ["AIService", "get_ai_service"]
