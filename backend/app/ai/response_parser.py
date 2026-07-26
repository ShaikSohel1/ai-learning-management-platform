"""
Response Parser & Validation Module.

Cleans raw LLM outputs (e.g. stripping markdown fenced blocks), parses JSON strings,
and validates structure using Pydantic schemas. Guarantees structured output integrity.
"""

import json
import logging
import re
from typing import Any, Dict
from pydantic import ValidationError

from app.schemas.ai import LearningPathResponse

logger = logging.getLogger(__name__)


class ResponseParser:
    """Parses and validates Gemini raw text outputs into structured Pydantic models."""

    @staticmethod
    def extract_json_string(raw_text: str) -> str:
        """
        Extracts JSON content from raw LLM output, handling markdown syntax ```json ... ``` blocks.
        """
        if not raw_text:
            return "{}"

        text = raw_text.strip()

        # Regex match for fenced markdown code block containing JSON
        pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # If text starts with { and ends with }, return as is
        first_brace = text.find("{")
        last_brace = text.rfind("}")
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            return text[first_brace : last_brace + 1]

        return text

    def parse_learning_path(self, raw_text: str, default_career_goal: str = "Target Role") -> LearningPathResponse:
        """
        Parses raw text into validated LearningPathResponse model.
        """
        cleaned_json = self.extract_json_string(raw_text)
        
        try:
            data = json.loads(cleaned_json)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error while parsing Gemini output: {e}. Raw text snippet: {cleaned_json[:200]}")
            return self._build_fallback_response(default_career_goal, f"Error parsing AI response: {e}")

        # Ensure dictionary
        if not isinstance(data, dict):
            logger.error(f"Parsed JSON is not a dictionary: {type(data)}")
            return self._build_fallback_response(default_career_goal, "Invalid JSON data structure returned from AI")

        # Validate with Pydantic
        try:
            validated = LearningPathResponse(**data)
            return validated
        except ValidationError as val_err:
            logger.warning(f"Pydantic validation warning on AI response: {val_err}. Sanitizing dictionary structure.")
            return self._sanitize_and_salvage(data, default_career_goal)

    def _sanitize_and_salvage(self, data: Dict[str, Any], default_goal: str) -> LearningPathResponse:
        """
        Attempts to salvage key fields from partial or slightly non-conforming dict.
        """
        career_goal = str(data.get("career_goal") or default_goal)
        estimated_duration = str(data.get("estimated_duration") or "4 Weeks")
        difficulty = str(data.get("difficulty") or "Intermediate")
        summary = str(data.get("summary") or f"Customized learning roadmap for {career_goal}.")

        raw_courses = data.get("recommended_courses", [])
        recommended_courses = []
        if isinstance(raw_courses, list):
            for c in raw_courses:
                if isinstance(c, dict):
                    recommended_courses.append({
                        "title": str(c.get("title") or "Recommended Module"),
                        "description": str(c.get("description") or "Targeted skill building course."),
                        "category": str(c.get("category") or "General"),
                        "difficulty": str(c.get("difficulty") or "Intermediate"),
                        "reason": str(c.get("reason") or "Fulfills core competency requirement.")
                    })

        raw_path = data.get("learning_path", [])
        learning_path = []
        if isinstance(raw_path, list):
            for idx, step in enumerate(raw_path, start=1):
                if isinstance(step, dict):
                    learning_path.append({
                        "week": int(step.get("week") or idx),
                        "topic": str(step.get("topic") or f"Week {idx} Milestones"),
                        "description": str(step.get("description") or "Focus on core concept implementation."),
                        "skills_to_acquire": list(step.get("skills_to_acquire") or [])
                    })

        return LearningPathResponse(
            career_goal=career_goal,
            recommended_courses=recommended_courses,
            learning_path=learning_path,
            estimated_duration=estimated_duration,
            difficulty=difficulty,
            summary=summary
        )

    def _build_fallback_response(self, career_goal: str, error_msg: str) -> LearningPathResponse:
        return LearningPathResponse(
            career_goal=career_goal,
            recommended_courses=[
                {
                    "title": "Foundational Skills Acceleration",
                    "description": "Essential core concepts and industry standard patterns.",
                    "category": "Core Engineering",
                    "difficulty": "Beginner",
                    "reason": "Establishes baseline knowledge required for career progression."
                }
            ],
            learning_path=[
                {
                    "week": 1,
                    "topic": "Fundamentals & Setup",
                    "description": "Environment configuration and foundational concepts.",
                    "skills_to_acquire": ["Core Principles", "Tooling Setup"]
                },
                {
                    "week": 2,
                    "topic": "Practical Project Implementation",
                    "description": "Hands-on implementation of target skills.",
                    "skills_to_acquire": ["Practical Engineering", "Best Practices"]
                }
            ],
            estimated_duration="2 Weeks",
            difficulty="Beginner",
            summary=f"Fallback roadmap generated for {career_goal}. ({error_msg})"
        )


response_parser = ResponseParser()
