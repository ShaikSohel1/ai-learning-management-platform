"""
AI Router Module.

Exposes RESTful endpoints for:
- POST /ai/learning-path : Generating structured learning path & course recommendations.
- POST /ai/chat          : General multi-turn conversational AI business assistant.
- DELETE /ai/history     : Clearing conversation history.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.ai import AIService, get_ai_service
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.ai import (
    AIChatRequest,
    AIChatResponse,
    LearningPathRequest,
    LearningPathResponse,
)

router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"]
)


@router.post(
    "/learning-path",
    response_model=LearningPathResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate personalized learning path and course recommendations"
)
def generate_learning_path(
    payload: LearningPathRequest,
    current_user: User = Depends(get_current_user),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Generates a structured career learning path based on candidate current skills and career goal.
    Returns structured JSON with recommended courses, weekly timeline, duration, and summary.
    """
    try:
        response = ai_service.generate_learning_path(
            career_goal=payload.career_goal,
            current_skills=payload.current_skills
        )
        return response
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate learning path: {exc!s}"
        )


@router.post(
    "/chat",
    response_model=AIChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Multi-turn AI Assistant Chat"
)
def chat_with_assistant(
    payload: AIChatRequest,
    current_user: User = Depends(get_current_user),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    General AI Business Assistant endpoint with context memory across requests.
    """
    try:
        response = ai_service.chat_with_assistant(
            user_id=current_user.id,
            message=payload.message,
            career_goal=payload.career_goal,
            current_skills=payload.current_skills
        )
        return response
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI chat assistant encountered an error: {exc!s}"
        )


@router.delete(
    "/history",
    status_code=status.HTTP_200_OK,
    summary="Clear user conversation memory history"
)
def clear_chat_history(
    current_user: User = Depends(get_current_user),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Resets and clears active conversation context memory for the authenticated user.
    """
    ai_service.clear_user_history(user_id=current_user.id)
    return {
        "success": True,
        "message": "Conversation history cleared successfully.",
        "user_id": current_user.id
    }


@router.get(
    "/model-status",
    status_code=status.HTTP_200_OK,
    summary="Get runtime discovered Gemini model registry and active fallback status"
)
def get_ai_model_status():
    """
    STEP 9 Endpoint: Returns active model, fallback status, available models, and health.
    """
    from app.ai.gemini_client import GeminiClient
    client = GeminiClient()
    return {
        "current_model": GeminiClient.get_active_model(),
        "fallback_enabled": True,
        "available_models": client.get_discovered_models(),
        "engine_health": "Operational"
    }

