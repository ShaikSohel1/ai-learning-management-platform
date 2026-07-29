"""
AI Service Facade Module.

Orchestrates Gemini Client, Prompt Manager, Response Parser, Retry Handler, and Conversation Memory.
Provides high-level business functions for generating learning paths and handling multi-turn AI assistant chats.
"""

import logging

from app.ai.conversation_memory import memory_store
from app.ai.gemini_client import GeminiClient
from app.ai.prompt_manager import prompt_manager
from app.ai.response_parser import response_parser
from app.ai.retry_handler import retry_handler
from app.schemas.ai import AIChatResponse, LearningPathResponse

logger = logging.getLogger(__name__)


class AIService:
    """Unified service facade for AI features in the LMS platform."""

    def __init__(self, gemini_client: GeminiClient | None = None) -> None:
        self.client = gemini_client or GeminiClient()

    def generate_learning_path(
        self,
        career_goal: str,
        current_skills: list[str],
        version: str | None = "V2"
    ) -> LearningPathResponse:
        """
        Generates a structured learning path for user's career goal and skills using versioned prompts.
        Applies exponential backoff retries and validates output against JSON schema.
        """
        prompt_builder = prompt_manager.get_learning_path_builder(
            career_goal=career_goal,
            current_skills=current_skills,
            version=version
        )
        user_prompt = prompt_builder.build_user_prompt()
        system_instruction = prompt_builder.get_system_instruction()

        logger.info(f"Generating AI learning path for goal='{career_goal}', skills={current_skills}")

        # Execute Gemini API call with exponential retry handler
        raw_output = retry_handler.execute(
            self.client.generate_content,
            prompt=user_prompt,
            system_instruction=system_instruction,
            json_mode=True
        )

        # Parse and validate structured output
        validated_response = response_parser.parse_learning_path(
            raw_text=raw_output,
            default_career_goal=career_goal
        )

        return validated_response

    def chat_with_assistant(
        self,
        user_id: int,
        message: str,
        career_goal: str | None = None,
        current_skills: list[str] | None = None
    ) -> AIChatResponse:
        """
        Processes multi-turn AI chat assistant queries using user conversation context memory.
        """
        # Fetch conversation context window
        history_context = memory_store.format_history_for_prompt(user_id)

        # Build prompt using PromptManager
        prompt_builder = prompt_manager.get_chat_builder(
            user_message=message,
            conversation_history=history_context,
            career_goal=career_goal,
            current_skills=current_skills,
            version="V1"
        )
        user_prompt = prompt_builder.build_user_prompt()
        system_instruction = prompt_builder.get_system_instruction()

        # Add user message to conversation memory store
        memory_store.add_user_message(user_id, message)

        logger.info(f"Processing AI assistant chat for user_id={user_id}")

        # Execute call with exponential backoff retry handler
        ai_reply = retry_handler.execute(
            self.client.generate_content,
            prompt=user_prompt,
            system_instruction=system_instruction,
            json_mode=False
        )

        # Add AI reply to conversation memory store
        memory_store.add_ai_message(user_id, ai_reply)

        current_history = memory_store.get_history(user_id)

        return AIChatResponse(
            response=ai_reply,
            history_length=len(current_history)
        )

    def clear_user_history(self, user_id: int) -> bool:
        """Clears stored multi-turn conversation context memory for specified user."""
        logger.info(f"Clearing conversation memory for user_id={user_id}")
        return memory_store.clear_history(user_id)


def get_ai_service() -> AIService:
    """Dependency injection helper for AIService."""
    return AIService()
