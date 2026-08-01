"""
Gemini Client Compatibility Module.

Re-exports GeminiProvider, AllGeminiModelsQuotaExhaustedError, and helper functions
for backward compatibility across legacy imports.
"""

from app.ai.providers.gemini_provider import (
    AllGeminiModelsQuotaExhaustedError,
    GeminiProvider,
)

# Backward-compatible class alias
GeminiClient = GeminiProvider


def generate_with_fallback(
    prompt: str,
    system_instruction: str | None = None,
    json_mode: bool = True
) -> str:
    """
    Backward-compatible wrapper function for executing Gemini API calls with automatic multi-model failover.
    """
    client = GeminiProvider()
    return client.generate_content(
        prompt=prompt,
        system_instruction=system_instruction,
        json_mode=json_mode
    )
