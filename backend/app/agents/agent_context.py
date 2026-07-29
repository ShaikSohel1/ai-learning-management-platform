"""
Agent Context Module.

Carries shared state, user profile, career goal, current skills, active DB session,
and intermediate step outputs across multi-agent workflow execution.
"""

from typing import Any

from sqlalchemy.orm import Session


class AgentContext:
    """Holds execution state passed between collaborating agents."""

    def __init__(
        self,
        user_id: int,
        user_name: str,
        user_email: str,
        user_role: str,
        query: str,
        career_goal: str | None = None,
        current_skills: list[str] | None = None,
        db: Session | None = None
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.user_role = user_role
        self.query = query
        self.career_goal = career_goal or "Backend Developer"
        self.current_skills = current_skills or []
        self.db = db

        # Shared accumulator dictionary for agent outputs
        self.state: dict[str, Any] = {}
        self.step_history: list[Any] = []

    def set(self, key: str, value: Any) -> None:
        self.state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)
