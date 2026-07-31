from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.rag import RAGService, get_rag_service
from app.schemas.knowledge import (
    DocumentMetadata,
    KnowledgeAnalyticsResponse,
    KnowledgeAskRequest,
    KnowledgeAskResponse,
    KnowledgeSearchResponse,
    SearchHistoryItem,
    SemanticSearchRequest,
)

router = APIRouter(
    prefix="/knowledge",
    tags=["Enterprise Knowledge Base"]
)


@router.post(
    "/upload",
    response_model=DocumentMetadata,
    status_code=status.HTTP_201_CREATED,
    summary="Upload enterprise document into vector knowledge base"
)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a filename.")

    allowed_exts = ("pdf", "txt", "md", "markdown", "docx")
    ext = file.filename.lower().split(".")[-1] if "." in file.filename else ""
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file extension '.{ext}'. Supported formats: .pdf, .txt, .md, .docx"
        )

    try:
        content_bytes = await file.read()
        metadata = rag_service.ingest_document(
            filename=file.filename,
            content_bytes=content_bytes,
            uploaded_by=current_user.name or current_user.email
        )
        return metadata
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest document: {exc!s}"
        )


@router.get(
    "/documents",
    response_model=list[DocumentMetadata],
    summary="List uploaded knowledge base documents"
)
def list_documents(
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service)
):
    return rag_service.get_all_documents()


@router.get(
    "/search",
    response_model=KnowledgeSearchResponse,
    summary="Search knowledge base vector similarity"
)
def search_knowledge_base(
    query: str = Query(..., min_length=2),
    top_k: int = Query(4, ge=1, le=10),
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service)
):
    citations, conf_score, proc_query = rag_service.retriever.hybrid_search(query=query, top_k=top_k)
    return KnowledgeSearchResponse(
        query=query,
        results_count=len(citations),
        confidence_score=conf_score,
        search_intent=proc_query.intent,
        citations=citations
    )


@router.post(
    "/semantic-search",
    response_model=KnowledgeSearchResponse,
    summary="Advanced hybrid semantic search"
)
def semantic_search(
    payload: SemanticSearchRequest,
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service)
):
    meta_filter = {"filename": payload.filename_filter} if payload.filename_filter else None
    citations, conf_score, proc_query = rag_service.retriever.hybrid_search(
        query=payload.query,
        top_k=payload.top_k or 4,
        threshold=payload.threshold if payload.threshold is not None else 0.3,
        metadata_filter=meta_filter
    )
    return KnowledgeSearchResponse(
        query=payload.query,
        results_count=len(citations),
        confidence_score=conf_score,
        search_intent=proc_query.intent,
        citations=citations
    )


@router.post(
    "/ask",
    response_model=KnowledgeAskResponse,
    summary="Ask Enterprise Knowledge Chat with RAG, citations, and confidence scoring"
)
def ask_knowledge_base(
    payload: KnowledgeAskRequest,
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service)
):
    try:
        response = rag_service.ask_question(
            question=payload.question,
            user_id=current_user.id,
            user_name=current_user.name or "Enterprise Learner",
            user_email=current_user.email or "user@enterprise.com",
            user_department=current_user.department or "Engineering",
            top_k=payload.top_k or 4,
            threshold=payload.threshold if payload.threshold is not None else 0.3
        )
        return response
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to answer question via Knowledge RAG: {exc!s}"
        )


@router.get(
    "/history",
    response_model=list[SearchHistoryItem],
    summary="Get user search history log"
)
def get_search_history(
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service)
):
    return rag_service.get_user_search_history(user_id=current_user.id)


@router.delete(
    "/history",
    summary="Clear user search history log"
)
def clear_search_history(
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service)
):
    rag_service.clear_user_search_history(user_id=current_user.id)
    return {
        "success": True,
        "message": "Search history log cleared successfully."
    }


@router.get(
    "/statistics",
    response_model=KnowledgeAnalyticsResponse,
    summary="Get Knowledge Base analytics metrics summary"
)
def get_statistics(
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service)
):
    return rag_service.get_statistics()


@router.post(
    "/reindex",
    summary="Re-index ChromaDB vector collection"
)
def reindex_collection(
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service)
):
    return rag_service.reindex_collection()


@router.delete(
    "/{document_id}",
    summary="Delete document from vector knowledge base"
)
def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service)
):
    deleted = rag_service.delete_document(document_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document ID not found in vector store.")
    return {
        "success": True,
        "message": f"Document '{document_id}' successfully deleted from Knowledge Base.",
        "document_id": document_id
    }
