"""
Gemini API Client Module.

Encapsulates authentication, HTTP payload formatting, and raw requests to Google's Gemini API endpoints.
Provides standard generation calls with JSON response mode configuration.
"""

import json
import logging
from typing import Any, Dict, Optional, List
import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiClient:
    """Low-level API client for Google Gemini LLM API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ) -> None:
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = model or settings.GEMINI_MODEL
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def generate_content(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        json_mode: bool = True
    ) -> str:
        """
        Sends a content generation request to Gemini REST API.

        Args:
            prompt: The full user/prompt text.
            system_instruction: Optional system instruction text.
            json_mode: If True, requests application/json output format.

        Returns:
            Raw response text from Gemini model.
        """
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            logger.warning("No valid GEMINI_API_KEY configured. Returning fallback mock response.")
            return self._generate_mock_fallback(prompt, json_mode)

        endpoint = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"

        contents = [{"parts": [{"text": prompt}]}]

        payload: Dict[str, Any] = {
            "contents": contents
        }

        generation_config: Dict[str, Any] = {
            "temperature": 0.3,
            "maxOutputTokens": 2048,
        }

        if json_mode:
            generation_config["responseMimeType"] = "application/json"

        payload["generationConfig"] = generation_config

        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        headers = {
            "Content-Type": "application/json"
        }

        with httpx.Client(timeout=30.0) as client:
            response = client.post(endpoint, json=payload, headers=headers)
            
            # Check for HTTP status errors (e.g. 429 rate limits, 500 server error)
            if response.status_code != 200:
                logger.error(f"Gemini API returned error code {response.status_code}: {response.text}")
                response.raise_for_status()

            data = response.json()
            try:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text
            except (KeyError, IndexError) as e:
                logger.error(f"Failed to parse Gemini API response payload structure: {data}")
                raise ValueError(f"Malformed response structure from Gemini API: {e}")

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
