"""
Report Generation Service Module.

Generates Learning Progress, Course, Skill Gap, and Knowledge Base Usage Reports in CSV and JSON formats.
"""

import io
import csv
from datetime import datetime, UTC
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.services.enrollment_service import get_user_enrollments
from app.rag import get_rag_service


class ReportService:
    """Generates analytics reports in CSV & JSON formats."""

    def generate_progress_csv(self, db: Session, user_id: int, user_name: str) -> str:
        enrollments = get_user_enrollments(db=db, user_id=user_id)
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(["Enrollment ID", "User Name", "Course Title", "Category", "Difficulty", "Status", "Progress %", "Started At", "Completed At"])
        
        for e in enrollments:
            c = e.course
            writer.writerow([
                e.id,
                user_name,
                c.title if c else "Unknown",
                c.category if c else "",
                c.difficulty if c else "",
                e.status,
                f"{e.progress_percentage}%",
                e.started_at.strftime("%Y-%m-%d") if e.started_at else "N/A",
                e.completed_at.strftime("%Y-%m-%d") if e.completed_at else "N/A"
            ])
            
        return output.getvalue()

    def generate_knowledge_usage_report(self) -> Dict[str, Any]:
        rag = get_rag_service()
        stats = rag.get_statistics()
        docs = rag.get_all_documents()

        return {
            "generated_at": datetime.now(UTC).isoformat(),
            "total_documents": stats.total_documents,
            "total_chunks": stats.total_chunks,
            "total_embeddings": stats.total_embeddings,
            "avg_response_latency_ms": stats.avg_response_time_ms,
            "avg_confidence_score": stats.avg_confidence_score,
            "documents_catalog": [
                {
                    "name": d.document_name,
                    "uploader": d.uploaded_by,
                    "chunks": d.chunk_count,
                    "size": d.document_size
                }
                for d in docs
            ]
        }


report_service = ReportService()
