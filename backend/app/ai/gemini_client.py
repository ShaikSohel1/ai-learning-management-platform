"""
Gemini API Client Module.

Encapsulates authentication and requests to Google's Gemini API using the official google-genai SDK.
Provides standard generation calls with JSON response mode configuration.
"""

import json
import logging
from typing import Any

from google import genai
from google.genai import types
from google.genai.errors import APIError

from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiClient:
    """Low-level API client for Google Gemini LLM API."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None
    ) -> None:
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = model or settings.GEMINI_MODEL
        
        # Initialize official Google GenAI Client if a valid key is present
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def generate_content(
        self,
        prompt: str,
        system_instruction: str | None = None,
        json_mode: bool = True
    ) -> str:
        """
        Sends a content generation request to Gemini API.

        Args:
            prompt: The full user/prompt text.
            system_instruction: Optional system instruction text.
            json_mode: If True, requests application/json output format.

        Returns:
            Raw response text from Gemini model.
        """
        if not self.client:
            logger.warning("No valid GEMINI_API_KEY configured. Returning fallback mock response.")
            return self._generate_mock_fallback(prompt, json_mode)

        # Configure model generation parameters
        config = types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=2048,
        )

        if json_mode:
            config.response_mime_type = "application/json"

        if system_instruction:
            config.system_instruction = system_instruction

        try:
            # Send request using the official SDK
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )
            
            if not response.text:
                logger.error(f"Gemini API returned an empty text response for model '{self.model}'.")
                raise ValueError(f"Gemini API returned an empty response for model '{self.model}'.")

            return response.text

        except APIError as e:
            logger.error(
                f"Gemini APIError [Code {getattr(e, 'code', 'Unknown')}]: {e.message if hasattr(e, 'message') else e}"
            )
            raise
        except Exception as e:
            logger.error(f"Unexpected error communicating with Gemini API: {e}")
            raise

    def _generate_mock_fallback(self, prompt: str, json_mode: bool) -> str:
        """
        Generates realistic fallback response when API key is unconfigured or in offline dev mode.
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
                    },
                    {
                        "title": "Docker, Kubernetes & Microservices Deployment",
                        "description": "Containerize backend services, manage multi-container orchestration, and setup CI/CD pipelines.",
                        "category": "DevOps & Cloud",
                        "difficulty": "Advanced",
                        "reason": "Essential for scaling backend applications in production environments."
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
                    },
                    {
                        "week": 3,
                        "topic": "Relational Databases & SQLAlchemy 2.0 ORM",
                        "description": "Design relational schemas, manage database migrations with Alembic, and optimize database queries.",
                        "skills_to_acquire": ["PostgreSQL", "SQLAlchemy", "Alembic"]
                    },
                    {
                        "week": 4,
                        "topic": "System Design, Microservices & Containerization",
                        "description": "Containerize services with Docker, handle message queues, and deploy robust cloud backends.",
                        "skills_to_acquire": ["Docker", "Redis", "Microservices Design"]
                    }
                ],
                "estimated_duration": "4 Weeks",
                "difficulty": "Intermediate",
                "summary": "This personalized learning path is tailored to bridge your existing technical background to a production-grade Backend Developer role. It focuses on modern async Python, database mastery, secure API architecture, and cloud deployment."
            }
            return json.dumps(fallback_obj)
        else:
            return "I am your AI Business Assistant. I can help you build custom learning paths, analyze skill gaps, recommend targeted courses, and provide career roadmap guidance!"
