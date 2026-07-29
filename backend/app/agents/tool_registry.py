"""
Tool Registry Module.

Wraps backend domain services (Course, Enrollment, Certificate, RAG Knowledge, Dashboard,
Notifications, Calendar, Email, Report Generation, Audit Logging) as executable tools for multi-agent calling.
"""

import logging
import time
from collections.abc import Callable
from typing import Any

from sqlalchemy.orm import Session

from app.rag import get_rag_service
from app.schemas.agents import ToolCallRecord
from app.services.audit_service import audit_service
from app.services.calendar_service import calendar_service
from app.services.course_service import get_all_courses
from app.services.email_service import email_service
from app.services.enrollment_service import (
    complete_enrollment,
    enroll_user,
    get_user_enrollments,
)
from app.services.notification_service import notification_service
from app.services.report_service import report_service

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Central registry exposing executable tools for specialized AI agents."""

    def __init__(self) -> None:
        self._tools: dict[str, dict[str, Any]] = {}
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        self.register_tool(
            name="course_search_tool",
            description="Searches LMS course catalog by search query, category, or difficulty level.",
            func=self._tool_course_search
        )
        self.register_tool(
            name="enroll_course_tool",
            description="Enrolls authenticated user into a specified course ID.",
            func=self._tool_enroll_course
        )
        self.register_tool(
            name="check_progress_tool",
            description="Fetches user's active enrollments and completion percentages.",
            func=self._tool_check_progress
        )
        self.register_tool(
            name="generate_certificate_tool",
            description="Marks course as completed and issues digital certificate.",
            func=self._tool_generate_certificate
        )
        self.register_tool(
            name="rag_knowledge_tool",
            description="Queries ChromaDB Enterprise Knowledge Base via Hybrid RAG search.",
            func=self._tool_rag_knowledge
        )
        self.register_tool(
            name="dashboard_stats_tool",
            description="Calculates user learning stats, completion rate, and active progress.",
            func=self._tool_dashboard_stats
        )
        self.register_tool(
            name="notification_tool",
            description="Creates in-app notification alerts for the user.",
            func=self._tool_notification
        )
        self.register_tool(
            name="calendar_tool",
            description="Generates weekly study plans and .ics calendar schedules.",
            func=self._tool_calendar
        )
        self.register_tool(
            name="email_tool",
            description="Sends transactional email notifications (Course completion, Reminders).",
            func=self._tool_email
        )
        self.register_tool(
            name="report_tool",
            description="Generates CSV/JSON learning progress & knowledge analytics reports.",
            func=self._tool_report
        )

    def register_tool(self, name: str, description: str, func: Callable[..., Any]) -> None:
        self._tools[name] = {
            "name": name,
            "description": description,
            "func": func
        }

    def execute_tool(self, name: str, **kwargs: Any) -> ToolCallRecord:
        start_time = time.perf_counter()
        tool_info = self._tools.get(name)
        clean_kwargs = {k: v for k, v in kwargs.items() if k != "db"}

        if not tool_info:
            elapsed = (time.perf_counter() - start_time) * 1000
            return ToolCallRecord(
                tool_name=name,
                tool_input=clean_kwargs,
                tool_output={"error": f"Tool '{name}' not found in registry."},
                execution_time_ms=round(elapsed, 2)
            )

        try:
            output = tool_info["func"](**kwargs)
            elapsed = (time.perf_counter() - start_time) * 1000

            # Audit log execution if db and user_id are present
            db_session = kwargs.get("db")
            uid = kwargs.get("user_id", 1)
            agent_name = kwargs.get("agent_name", "AI Action Assistant")

            if db_session:
                try:
                    audit_service.log_execution(
                        db=db_session,
                        user_id=uid,
                        agent_name=agent_name,
                        tool_name=name,
                        execution_time_ms=round(elapsed, 2),
                        status="SUCCESS"
                    )
                except Exception:
                    pass

            return ToolCallRecord(
                tool_name=name,
                tool_input=clean_kwargs,
                tool_output=output,
                execution_time_ms=round(elapsed, 2)
            )
        except Exception as e:
            elapsed = (time.perf_counter() - start_time) * 1000
            logger.error(f"Error executing tool '{name}': {e}")
            return ToolCallRecord(
                tool_name=name,
                tool_input=clean_kwargs,
                tool_output={"error": str(e)},
                execution_time_ms=round(elapsed, 2)
            )

    def list_tools(self) -> list[dict[str, str]]:
        return [
            {"name": t["name"], "description": t["description"]}
            for t in self._tools.values()
        ]

    # Tool Implementation Functions
    def _tool_course_search(self, db: Session, query: str = "", category: str = "") -> list[dict[str, Any]]:
        courses = get_all_courses(db=db, search=query or None, category=category or None, limit=10)
        return [
            {
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "category": c.category,
                "duration": c.duration,
                "difficulty": c.difficulty
            }
            for c in courses
        ]

    def _tool_enroll_course(self, db: Session, user_id: int, course_id: int) -> dict[str, Any]:
        enrollment = enroll_user(db=db, user_id=user_id, course_id=course_id)
        
        # Trigger Notification
        try:
            notification_service.create_notification(
                db=db,
                user_id=user_id,
                title="🎓 Course Enrolled",
                message=f"You have been successfully enrolled in course ID {course_id}.",
                notification_type="INFO"
            )
        except Exception:
            pass

        return {
            "enrollment_id": enrollment.id,
            "user_id": enrollment.user_id,
            "course_id": enrollment.course_id,
            "status": enrollment.status,
            "progress_percentage": enrollment.progress_percentage
        }

    def _tool_check_progress(self, db: Session, user_id: int) -> list[dict[str, Any]]:
        enrollments = get_user_enrollments(db=db, user_id=user_id)
        return [
            {
                "enrollment_id": e.id,
                "course_id": e.course_id,
                "course_title": e.course.title if e.course else "",
                "status": e.status,
                "progress_percentage": e.progress_percentage,
                "certificate_generated": e.certificate_generated
            }
            for e in enrollments
        ]

    def _tool_generate_certificate(self, db: Session, user_id: int, enrollment_id: int) -> dict[str, Any]:
        enrollment = complete_enrollment(db=db, enrollment_id=enrollment_id, user_id=user_id)
        
        try:
            notification_service.create_notification(
                db=db,
                user_id=user_id,
                title="🏆 Certificate Issued",
                message=f"Digital certificate issued for enrollment #{enrollment.id}.",
                notification_type="CERTIFICATE"
            )
        except Exception:
            pass

        return {
            "enrollment_id": enrollment.id,
            "status": enrollment.status,
            "certificate_generated": enrollment.certificate_generated
        }

    def _tool_rag_knowledge(self, question: str) -> dict[str, Any]:
        rag = get_rag_service()
        res = rag.ask_question(question=question, top_k=4)
        return {
            "answer": res.answer,
            "rag_used": res.rag_used,
            "confidence_score": res.confidence_score,
            "citations_count": len(res.citations),
            "referenced_documents": res.referenced_documents
        }

    def _tool_dashboard_stats(self, db: Session, user_id: int) -> dict[str, Any]:
        enrollments = get_user_enrollments(db=db, user_id=user_id)
        total = len(enrollments)
        completed = sum(1 for e in enrollments if e.status == "COMPLETED")
        in_progress = sum(1 for e in enrollments if e.status == "IN_PROGRESS")
        rate = round((completed / total) * 100, 1) if total > 0 else 0.0

        return {
            "total_enrolled": total,
            "in_progress": in_progress,
            "completed": completed,
            "completion_rate": rate,
            "risk_level": "LOW" if rate >= 50 else ("MEDIUM" if rate >= 20 else "HIGH")
        }

    def _tool_notification(self, db: Session, user_id: int, title: str, message: str, notification_type: str = "INFO") -> dict[str, Any]:
        notif = notification_service.create_notification(
            db=db,
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type
        )
        return {"notification_id": notif.id, "title": notif.title, "status": "CREATED"}

    def _tool_calendar(self, course_title: str = "Backend Architecture", weeks: int = 4) -> dict[str, Any]:
        return calendar_service.generate_study_plan(course_title=course_title, weeks=weeks)

    def _tool_email(self, to_email: str, user_name: str, course_title: str, email_type: str = "reminder") -> dict[str, Any]:
        if email_type == "completion":
            return email_service.send_course_completion_email(to_email=to_email, user_name=user_name, course_title=course_title, certificate_number="CERT-9981")
        else:
            return email_service.send_learning_reminder_email(to_email=to_email, user_name=user_name, course_title=course_title)

    def _tool_report(self, db: Session, user_id: int, user_name: str = "Learner") -> dict[str, Any]:
        csv_data = report_service.generate_progress_csv(db=db, user_id=user_id, user_name=user_name)
        usage_data = report_service.generate_knowledge_usage_report()
        return {
            "csv_rows_count": len(csv_data.splitlines()),
            "usage_report": usage_data,
            "status": "GENERATED"
        }


tool_registry = ToolRegistry()
