"""
Base Agent Abstract Class Module.

Defines standard interface contract for all specialized agents in the Agentic AI platform.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from app.schemas.agents import AgentStepResult

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class for specialized AI agents."""

    def __init__(
        self,
        name: str,
        role: str,
        description: str,
        tools: list[str]
    ):
        self.name = name
        self.role = role
        self.description = description
        self.tools = tools

    @abstractmethod
    def execute(self, context: Any) -> AgentStepResult:
        """
        Executes agent's specialized task given shared AgentContext.
        Returns structured AgentStepResult.
        """
