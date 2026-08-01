"""
Health Monitoring Router Module.

Provides granular health check endpoints for Database, Multi-Provider Multi-Model AI Engine,
ChromaDB Vector Store, and overall System Health status.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.ai.llm_manager import llm_manager
from app.core.config import settings
from app.database.database import get_db
from app.rag import RAGService, get_rag_service

router = APIRouter(
    tags=["Health Monitoring"]
)


@router.get(
    "/health",
    summary="General application health status"
)
def get_health():
    return {
        "status": "HEALTHY",
        "service": "AI Learning Management Platform API",
        "version": "1.0.0"
    }


@router.get(
    "/system/info",
    summary="Get active AI provider, model, and system status"
)
def get_system_info():
    h = llm_manager.get_health_status()
    return {
        "provider": h["current_provider"],
        "model": h["current_model"],
        "status": h["failover_status"]
    }


@router.get(
    "/health/database",
    summary="PostgreSQL database connectivity check"
)
def check_database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "component": "PostgreSQL Database",
            "status": "HEALTHY",
            "message": "Database connection verified."
        }
    except Exception as e:
        return {
            "component": "PostgreSQL Database",
            "status": "DEGRADED",
            "error": str(e)
        }


@router.get(
    "/health/ai",
    summary="Multi-Provider Multi-Model AI Engine connectivity check"
)
def check_ai_health():
    """
    Returns real-time health diagnostic metrics for Groq & Gemini providers, model chains, and failover status.
    """
    return llm_manager.get_health_status()


@router.get(
    "/health/vector",
    summary="ChromaDB vector store check"
)
def check_vector_store_health(rag_service: RAGService = Depends(get_rag_service)):
    try:
        metadatas = rag_service.vector_db.list_all_metadatas()
        return {
            "component": "ChromaDB Vector Store",
            "status": "HEALTHY",
            "persisted_chunks": len(metadatas),
            "collection_name": rag_service.vector_db.collection_name
        }
    except Exception as e:
        return {
            "component": "ChromaDB Vector Store",
            "status": "DEGRADED",
            "error": str(e)
        }


@router.get(
    "/status",
    summary="Comprehensive system status dashboard"
)
def get_full_system_status(
    db: Session = Depends(get_db),
    rag_service: RAGService = Depends(get_rag_service)
):
    db_ok = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_ok = False

    vector_ok = True
    try:
        rag_service.vector_db.list_all_metadatas()
    except Exception:
        vector_ok = False

    overall = "HEALTHY" if (db_ok and vector_ok) else "DEGRADED"

    h = llm_manager.get_health_status()
    return {
        "overall_status": overall,
        "database": "HEALTHY" if db_ok else "DEGRADED",
        "vector_store": "HEALTHY" if vector_ok else "DEGRADED",
        "ai_engine": h["failover_status"],
        "agents_platform": "HEALTHY",
        "provider": h["current_provider"],
        "model": h["current_model"]
    }
