"""
Base Agent Abstract Class Module.

Defines standard interface contract for all specialized agents in the Agentic AI platform.
"""

from abc import ABC, abstractmethod
import logging
from typing import List, Dict, Any

from app.schemas.agents import AgentStepResult, ToolCallRecord

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class for specialized AI agents."""

    def __init__(
        self,
        name: str,
        role: str,
        description: str,
        tools: List[str]
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
        pass
