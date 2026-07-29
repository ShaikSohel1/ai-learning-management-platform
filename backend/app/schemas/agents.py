from typing import Any

from pydantic import BaseModel, Field


class ToolCallRecord(BaseModel):
    tool_name: str = Field(..., description="Name of the executed tool")
    tool_input: dict[str, Any] = Field(default_factory=dict, description="Input parameters passed to the tool")
    tool_output: Any = Field(None, description="Result output returned by the tool")
    execution_time_ms: float = Field(0.0, description="Latency in milliseconds")


class AgentStepResult(BaseModel):
    agent_name: str = Field(..., description="Name of the specialized agent")
    agent_role: str = Field(..., description="Role responsibility of the agent")
    status: str = Field("COMPLETED", description="Status: PENDING, RUNNING, COMPLETED, FAILED")
    reasoning: str = Field(..., description="Agent reasoning or output summary")
    structured_data: dict[str, Any] | None = Field(default_factory=dict, description="Structured data returned by agent")
    tool_calls: list[ToolCallRecord] = Field(default_factory=list, description="Tool calls executed during step")
    confidence_score: float = Field(..., description="Confidence score (0.0 to 100.0%)")
    execution_time_ms: float = Field(0.0, description="Latency in milliseconds")


class AgentChatRequest(BaseModel):
    message: str = Field(..., min_length=2, description="User goal or query string", example="I want to become a Backend Developer")
    career_goal: str | None = Field(None, description="Optional career goal context")
    current_skills: list[str] | None = Field(default_factory=list, description="Optional user skills context")


class AgentChatResponse(BaseModel):
    user_query: str
    workflow_intent: str
    active_agent: str
    overall_confidence: float
    total_execution_time_ms: float
    final_summary: str
    steps: list[AgentStepResult]
    recommended_action: dict[str, Any] | None = None


class AgentWorkflowRequest(BaseModel):
    pipeline_type: str = Field(..., description="Pipeline type: career_transformation, skill_assessment, course_discovery, knowledge_search")
    career_goal: str
    current_skills: list[str] = Field(default_factory=list)


class AgentExecuteToolRequest(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class AgentStatusInfo(BaseModel):
    agent_name: str
    role: str
    description: str
    available_tools: list[str]


class AgentSystemStatusResponse(BaseModel):
    status: str
    total_agents: int
    agents: list[AgentStatusInfo]
    registered_tools_count: int
