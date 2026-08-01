"""
Provider Manager Compatibility Module.

Re-exports LLMManager and llm_manager instance for backward compatibility.
"""

from app.ai.llm_manager import LLMManager, get_llm_manager, llm_manager

# Backward-compatible class & instance aliases
AIProviderManager = LLMManager
provider_manager = llm_manager
get_provider_manager = get_llm_manager
