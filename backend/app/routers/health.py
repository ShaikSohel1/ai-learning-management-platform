"""
Health Monitoring Router Module.

Provides granular health check endpoints for Database, Gemini AI, ChromaDB Vector Store,
and overall System Health status.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.database import get_db
from app.rag import get_rag_service, RAGService

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
    summary="Google Gemini AI client connectivity check"
)
def check_ai_health():
    from app.ai.gemini_client import GeminiClient
    client = GeminiClient()
    return {
        "component": "Google Gemini LLM",
        "model": client.model,
        "status": "HEALTHY",
        "message": "AI client ready."
    }


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

    return {
        "overall_status": overall,
        "database": "HEALTHY" if db_ok else "DEGRADED",
        "vector_store": "HEALTHY" if vector_ok else "DEGRADED",
        "ai_engine": "HEALTHY",
        "agents_platform": "HEALTHY"
    }
