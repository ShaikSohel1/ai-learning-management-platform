"""
Agent Manager & Intelligent Router Module.

Maintains registry of all specialized agents and determines optimal single or multi-agent routing
based on user intent classification.
"""

import logging

from app.agents.base_agent import BaseAgent
from app.agents.specialized_agents import (
    AssessmentAgent,
    CareerPlannerAgent,
    CertificateAgent,
    CourseRecommendationAgent,
    DashboardInsightsAgent,
    EnrollmentAgent,
    KnowledgeAgent,
    SkillGapAgent,
)

logger = logging.getLogger(__name__)


Tuple_Pipeline = tuple[str, str, list[BaseAgent]]


class AgentManager:
    """Central registry and intelligent router for all specialized platform agents."""

    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}
        self._register_agents()

    def _register_agents(self) -> None:
        agents_list: list[BaseAgent] = [
            CareerPlannerAgent(),
            SkillGapAgent(),
            CourseRecommendationAgent(),
            AssessmentAgent(),
            EnrollmentAgent(),
            KnowledgeAgent(),
            CertificateAgent(),
            DashboardInsightsAgent(),
        ]

        for ag in agents_list:
            self._agents[ag.name] = ag

    def get_agent(self, name: str) -> BaseAgent | None:
        return self._agents.get(name)

    def list_agents(self) -> list[BaseAgent]:
        return list(self._agents.values())

    def route_query(self, query: str) -> Tuple_Pipeline:
        """
        Determines intent and selects the optimal list of specialized agents to execute.

        Returns: (intent_name, active_primary_agent_name, list_of_agents_to_run)
        """
        q = query.lower()

        if any(w in q for w in ["enroll", "register", "join course", "take course"]):
            return "enrollment_action", "Enrollment Agent", [self._agents["Enrollment Agent"], self._agents["Course Recommendation Agent"]]

        elif any(w in q for w in ["leave", "policy", "sop", "handbook", "document", "compliance"]):
            return "knowledge_search", "Knowledge Agent", [self._agents["Knowledge Agent"]]

        elif any(w in q for w in ["ready", "assessment", "quiz", "test", "evaluate", "project"]):
            return "skill_assessment", "Assessment Agent", [self._agents["Assessment Agent"], self._agents["Skill Gap Agent"]]

        elif any(w in q for w in ["certificate", "completion", "degree", "diploma"]):
            return "certificate_verification", "Certificate Agent", [self._agents["Certificate Agent"], self._agents["Enrollment Agent"]]

        elif any(w in q for w in ["stats", "progress", "risk", "dashboard", "analytics", "streak"]):
            return "dashboard_insights", "Dashboard Insights Agent", [self._agents["Dashboard Insights Agent"]]

        else:
            # Default: Full Multi-Agent Career Transformation Pipeline
            return "career_transformation", "Career Planner Agent", [
                self._agents["Career Planner Agent"],
                self._agents["Skill Gap Agent"],
                self._agents["Course Recommendation Agent"],
                self._agents["Knowledge Agent"],
                self._agents["Assessment Agent"],
                self._agents["Dashboard Insights Agent"],
            ]


Tuple_Pipeline = tuple[str, str, list[BaseAgent]]

agent_manager = AgentManager()
