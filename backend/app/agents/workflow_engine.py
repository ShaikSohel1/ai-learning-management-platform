"""
Workflow Engine Module.

Orchestrates multi-agent workflow execution, passes context between collaborating agents,
synthesizes unified executive responses via AIProviderManager, and calculates execution metrics.
"""

import logging
import time

from sqlalchemy.orm import Session

from app.agents.agent_context import AgentContext
from app.agents.agent_manager import agent_manager
from app.agents.agent_memory import agent_memory_store
from app.ai.provider_manager import AIProviderManager, provider_manager
from app.ai.retry_handler import retry_handler
from app.schemas.agents import AgentChatResponse, AgentStepResult

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """Orchestrates collaborative multi-agent workflow pipelines."""

    def __init__(self, ai_provider_manager: AIProviderManager | None = None) -> None:
        self.provider = ai_provider_manager or provider_manager
        self.client = self.provider
        self.manager = agent_manager
        self.memory = agent_memory_store

    def execute_workflow(
        self,
        user_id: int,
        user_name: str,
        user_email: str,
        user_role: str,
        query: str,
        career_goal: str | None = None,
        current_skills: list[str] | None = None,
        db: Session | None = None
    ) -> AgentChatResponse:
        start_time = time.perf_counter()

        # Step 1: Intelligent Routing
        intent_name, primary_agent_name, agents_to_run = self.manager.route_query(query)

        # Step 2: Initialize Agent Context
        context = AgentContext(
            user_id=user_id,
            user_name=user_name,
            user_email=user_email,
            user_role=user_role,
            query=query,
            career_goal=career_goal or "Backend Developer",
            current_skills=current_skills or [],
            db=db
        )

        logger.info(f"Executing Agentic Workflow intent='{intent_name}' with {len(agents_to_run)} specialized agents for user_id={user_id}")

        step_results: list[AgentStepResult] = []

        # Step 3: Sequential Agent Execution & Communication
        for agent in agents_to_run:
            try:
                res = agent.execute(context)
                step_results.append(res)

                # Record decision in shared agent memory
                self.memory.record_decision(
                    user_id=user_id,
                    agent_name=agent.name,
                    decision_summary=res.reasoning,
                    output_data=res.structured_data or {}
                )
            except Exception as e:
                logger.error(f"Error running agent '{agent.name}': {e}")

        # Step 4: Synthesize Final Unified Response
        total_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        overall_confidence = (
            round(sum(r.confidence_score for r in step_results) / len(step_results), 1)
            if step_results else 90.0
        )

        summaries = [f"• [{r.agent_name}]: {r.reasoning}" for r in step_results]
        system_instruction = (
            "You are the Lead Enterprise Multi-Agent Orchestrator. "
            "Synthesize the outputs of all collaborating specialized AI agents into a polished, professional executive summary. "
            "Highlight key career goals, skill gaps, course recommendations, and next action steps clearly."
        )

        prompt = (
            f"USER QUERY / GOAL: {query}\n"
            f"CAREER ROLE TARGET: {context.career_goal}\n"
            f"COLLABORATING AGENT OUTPUTS:\n" + "\n".join(summaries) + "\n\n"
            "INSTRUCTIONS:\nProvide a cohesive, encouraging, structured final executive answer."
        )

        final_summary = retry_handler.execute(
            self.provider.generate_content,
            prompt=prompt,
            system_instruction=system_instruction,
            json_mode=False
        )

        # Formulate recommended 1-click executable action if available
        recs = context.get("recommended_courses", [])
        rec_action = None
        if recs:
            rec_action = {
                "action_type": "ENROLL",
                "course_id": recs[0]["course_id"],
                "course_title": recs[0]["title"],
                "label": f"🎓 Enroll Now in {recs[0]['title']}"
            }

        return AgentChatResponse(
            user_query=query,
            workflow_intent=intent_name,
            active_agent=primary_agent_name,
            overall_confidence=overall_confidence,
            total_execution_time_ms=total_time_ms,
            final_summary=final_summary,
            steps=step_results,
            recommended_action=rec_action
        )


workflow_engine = WorkflowEngine()


def get_workflow_engine() -> WorkflowEngine:
    return workflow_engine
