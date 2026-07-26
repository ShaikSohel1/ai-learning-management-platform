from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.agents import (
    AgentChatRequest,
    AgentChatResponse,
    AgentWorkflowRequest,
    AgentExecuteToolRequest,
    AgentSystemStatusResponse,
    AgentStatusInfo,
)
from app.agents import (
    workflow_engine,
    get_workflow_engine,
    WorkflowEngine,
    agent_manager,
    tool_registry,
    agent_memory_store,
)
from app.services.audit_service import audit_service
from app.services.calendar_service import calendar_service
from app.services.report_service import report_service

router = APIRouter(
    prefix="/agents",
    tags=["Agentic AI Platform"]
)


@router.post(
    "/chat",
    response_model=AgentChatResponse,
    summary="Process user query via Multi-Agent Collaborative Platform"
)
def agent_chat(
    payload: AgentChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    engine: WorkflowEngine = Depends(get_workflow_engine)
):
    try:
        response = engine.execute_workflow(
            user_id=current_user.id,
            user_name=current_user.name or current_user.email,
            user_email=current_user.email,
            user_role=current_user.role,
            query=payload.message,
            career_goal=payload.career_goal,
            current_skills=payload.current_skills,
            db=db
        )
        return response
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent workflow execution error: {str(exc)}"
        )


@router.post(
    "/workflow",
    response_model=AgentChatResponse,
    summary="Execute specific multi-agent pipeline workflow"
)
def execute_workflow_pipeline(
    payload: AgentWorkflowRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    engine: WorkflowEngine = Depends(get_workflow_engine)
):
    query = f"Execute pipeline '{payload.pipeline_type}' for target role '{payload.career_goal}'"
    return engine.execute_workflow(
        user_id=current_user.id,
        user_name=current_user.name or current_user.email,
        user_email=current_user.email,
        user_role=current_user.role,
        query=query,
        career_goal=payload.career_goal,
        current_skills=payload.current_skills,
        db=db
    )


@router.get(
    "/status",
    response_model=AgentSystemStatusResponse,
    summary="Get status of all specialized platform agents"
)
def get_agents_status(
    current_user: User = Depends(get_current_user)
):
    agents = agent_manager.list_agents()
    status_list = [
        AgentStatusInfo(
            agent_name=a.name,
            role=a.role,
            description=a.description,
            available_tools=a.tools
        )
        for a in agents
    ]

    return AgentSystemStatusResponse(
        status="ACTIVE",
        total_agents=len(agents),
        agents=status_list,
        registered_tools_count=len(tool_registry.list_tools())
    )


@router.get(
    "/tools",
    summary="List available executable tools in Tool Registry"
)
def list_available_tools(
    current_user: User = Depends(get_current_user)
):
    return {
        "tools_count": len(tool_registry.list_tools()),
        "tools": tool_registry.list_tools()
    }


@router.post(
    "/execute",
    summary="Execute direct tool call"
)
def execute_direct_tool(
    payload: AgentExecuteToolRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    args = payload.arguments or {}
    args["db"] = db
    args["user_id"] = current_user.id
    args["agent_name"] = "Direct Tool Calling"

    result = tool_registry.execute_tool(payload.tool_name, **args)
    return result.dict()


@router.get(
    "/history",
    summary="Get user agent memory decision history logs"
)
def get_user_agent_history(
    current_user: User = Depends(get_current_user)
):
    return agent_memory_store.get_memory_summary(current_user.id)


@router.get(
    "/audit-logs",
    summary="Get user agent tool execution audit logs"
)
def get_audit_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logs = audit_service.get_user_audit_logs(db=db, user_id=current_user.id)
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "agent_name": log.agent_name,
            "tool_name": log.tool_name,
            "status": log.status,
            "execution_time_ms": log.execution_time_ms,
            "timestamp": log.created_at.isoformat() if log.created_at else ""
        }
        for log in logs
    ]


@router.get(
    "/calendar/export-ics",
    summary="Export iCalendar (.ics) study plan file"
)
def export_ics(
    course_title: str = "Backend Architecture",
    current_user: User = Depends(get_current_user)
):
    ics_content = calendar_service.export_ics_calendar(
        course_title=course_title,
        user_name=current_user.name or current_user.email
    )
    return Response(
        content=ics_content,
        media_type="text/calendar",
        headers={"Content-Disposition": f"attachment; filename=study_schedule.ics"}
    )


@router.get(
    "/reports/progress-csv",
    summary="Export Learning Progress CSV report"
)
def export_progress_csv(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    csv_content = report_service.generate_progress_csv(
        db=db,
        user_id=current_user.id,
        user_name=current_user.name or current_user.email
    )
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=learning_progress_report.csv"}
    )
