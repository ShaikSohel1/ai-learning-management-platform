"""
Audit Logging Service Module.

Records agent tool executions in database for compliance and auditing.
"""


from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditService:
    """Service tracking agent tool executions in PostgreSQL database."""

    def log_execution(
        self,
        db: Session,
        user_id: int,
        agent_name: str,
        tool_name: str,
        execution_time_ms: float,
        status: str = "SUCCESS"
    ) -> AuditLog:
        log = AuditLog(
            user_id=user_id,
            agent_name=agent_name,
            tool_name=tool_name,
            status=status,
            execution_time_ms=execution_time_ms
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    def get_user_audit_logs(self, db: Session, user_id: int) -> list[AuditLog]:
        return (
            db.query(AuditLog)
            .filter(AuditLog.user_id == user_id)
            .order_by(AuditLog.created_at.desc())
            .limit(30)
            .all()
        )


audit_service = AuditService()
