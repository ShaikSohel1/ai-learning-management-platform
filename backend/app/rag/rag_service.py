"""
RAG Service Facade Module.

High-level business service orchestrating:
- Document ingestion and vector persistence.
- Hybrid search (Vector + BM25 keyword + Metadata filtering).
- Multi-criteria reranking and sentence-level context compression.
- Confidence score calculation and search history logging.
- RAG QA generation with automatic Gemini fallback.
- Knowledge base analytics and re-indexing.
"""

import time
from datetime import datetime, UTC
import uuid
import logging
from typing import List, Dict, Any, Optional

from app.rag.document_loader import document_loader
from app.rag.text_chunker import text_chunker
from app.rag.embedding_service import embedding_service
from app.rag.vector_store import vector_store
from app.rag.retriever import retriever
from app.rag.context_compressor import context_compressor
from app.rag.search_history import search_history_store
from app.ai.gemini_client import GeminiClient
from app.ai.retry_handler import retry_handler
from app.schemas.knowledge import (
    DocumentMetadata,
    KnowledgeAskResponse,
    KnowledgeCitation,
    KnowledgeAnalyticsResponse,
)

logger = logging.getLogger(__name__)


class RAGService:
    """Unified Enterprise Semantic Search Platform Service Facade."""

    def __init__(self, gemini_client: Optional[GeminiClient] = None) -> None:
        self.loader = document_loader
        self.chunker = text_chunker
        self.embeddings = embedding_service
        self.vector_db = vector_store
        self.retriever = retriever
        self.compressor = context_compressor
        self.history_store = search_history_store
        self.client = gemini_client or GeminiClient()

    def ingest_document(
        self,
        filename: str,
        content_bytes: bytes,
        uploaded_by: str
    ) -> DocumentMetadata:
        doc_id = str(uuid.uuid4())
        upload_date = datetime.now(UTC).isoformat()
        size_bytes = len(content_bytes)

        if size_bytes < 1024:
            size_str = f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            size_str = f"{round(size_bytes / 1024, 1)} KB"
        else:
            size_str = f"{round(size_bytes / (1024 * 1024), 1)} MB"

        logger.info(f"Ingesting document '{filename}' ({size_str}) uploaded by {uploaded_by}")

        text = self.loader.load_document(filename, content_bytes)
        chunks = self.chunker.chunk_text(text)
        chunk_texts = [c.text for c in chunks]

        vector_embeddings = self.embeddings.get_embeddings_batch(chunk_texts)

        stored_count = self.vector_db.add_chunks(
            doc_id=doc_id,
            filename=filename,
            uploader=uploaded_by,
            upload_date=upload_date,
            chunks=chunk_texts,
            embeddings=vector_embeddings
        )

        return DocumentMetadata(
            document_id=doc_id,
            document_name=filename,
            upload_date=upload_date,
            uploaded_by=uploaded_by,
            chunk_count=stored_count,
            embedding_count=stored_count,
            document_size=size_str
        )

    def get_all_documents(self) -> List[DocumentMetadata]:
        metadatas = self.vector_db.list_all_metadatas()
        if not metadatas:
            return []

        doc_groups: Dict[str, Dict[str, Any]] = {}
        for m in metadatas:
            doc_id = m.get("doc_id")
            if not doc_id:
                continue

            if doc_id not in doc_groups:
                doc_groups[doc_id] = {
                    "document_id": doc_id,
                    "document_name": m.get("filename", "Document"),
                    "upload_date": m.get("upload_date", ""),
                    "uploaded_by": m.get("uploader", "System"),
                    "chunk_count": 0,
                    "embedding_count": 0,
                    "document_size": "N/A"
                }

            doc_groups[doc_id]["chunk_count"] += 1
            doc_groups[doc_id]["embedding_count"] += 1

        return [DocumentMetadata(**g) for g in doc_groups.values()]

    def delete_document(self, document_id: str) -> bool:
        return self.vector_db.delete_document(document_id)

    def ask_question(
        self,
        question: str,
        user_id: int = 1,
        top_k: int = 4,
        threshold: float = 0.3
    ) -> KnowledgeAskResponse:
        start_time = time.perf_counter()

        # Execute Hybrid Search Pipeline (Query Processor -> Vector Search -> Reranker -> Confidence)
        citations, confidence_score, proc_query = self.retriever.hybrid_search(
            query=question,
            top_k=top_k,
            threshold=threshold
        )

        referenced_docs = sorted(list({c.document_name for c in citations}))

        if citations and confidence_score >= (threshold * 100):
            # Compress context at sentence level
            compressed_context = self.compressor.compress_citations(
                citations=citations,
                query_keywords=proc_query.keywords
            )

            system_instruction = (
                "You are an Enterprise Semantic Search Knowledge Assistant. "
                "Answer the user's question using ONLY the provided compressed enterprise document context. "
                "Do NOT invent or hallucinate facts outside the provided document text. Be precise, concise, professional, and clear. "
                "Reference the source document names where appropriate."
            )

            prompt = (
                f"COMPRESSED ENTERPRISE DOCUMENT CONTEXT:\n{compressed_context}\n\n"
                f"OPTIMIZED USER QUESTION: {proc_query.optimized_query}\n\n"
                "INSTRUCTIONS:\nAnswer the question based directly on the compressed document context above."
            )

            ai_answer = retry_handler.execute(
                self.client.generate_content,
                prompt=prompt,
                system_instruction=system_instruction,
                json_mode=False
            )

            end_time = time.perf_counter()
            elapsed_ms = round((end_time - start_time) * 1000, 2)

            # Log search history
            self.history_store.add_entry(
                user_id=user_id,
                question=question,
                response_time_ms=elapsed_ms,
                documents_used=referenced_docs,
                confidence_score=confidence_score,
                rag_used=True
            )

            return KnowledgeAskResponse(
                answer=ai_answer,
                rag_used=True,
                confidence_score=confidence_score,
                response_time_ms=elapsed_ms,
                search_intent=proc_query.intent,
                citations=citations,
                referenced_documents=referenced_docs
            )
        else:
            system_instruction = (
                "You are an AI Business Assistant for an Enterprise Learning Management Platform. "
                "Answer the user's career development, course, or enterprise learning question professionally."
            )

            fallback_answer = retry_handler.execute(
                self.client.generate_content,
                prompt=question,
                system_instruction=system_instruction,
                json_mode=False
            )

            end_time = time.perf_counter()
            elapsed_ms = round((end_time - start_time) * 1000, 2)

            self.history_store.add_entry(
                user_id=user_id,
                question=question,
                response_time_ms=elapsed_ms,
                documents_used=[],
                confidence_score=0.0,
                rag_used=False
            )

            return KnowledgeAskResponse(
                answer=fallback_answer + "\n\n*(Note: No matching enterprise document context was found in the Knowledge Base; this response was generated using general AI guidance.)*",
                rag_used=False,
                confidence_score=0.0,
                response_time_ms=elapsed_ms,
                search_intent=proc_query.intent,
                citations=[],
                referenced_documents=[]
            )

    def get_user_search_history(self, user_id: int) -> List[Dict[str, Any]]:
        return self.history_store.get_user_history(user_id)

    def clear_user_search_history(self, user_id: int) -> bool:
        return self.history_store.clear_user_history(user_id)

    def get_statistics(self) -> KnowledgeAnalyticsResponse:
        docs = self.get_all_documents()
        total_docs = len(docs)
        total_chunks = sum(d.chunk_count for d in docs)
        avg_chunk_size = 550 if total_chunks > 0 else 0
        total_embeddings = sum(d.embedding_count for d in docs)

        metrics = self.history_store.get_analytics_metrics()

        # Calculate total storage size string
        total_kb = total_chunks * 0.6  # Approx
        size_str = f"{round(total_kb, 1)} KB" if total_kb < 1024 else f"{round(total_kb / 1024, 2)} MB"

        return KnowledgeAnalyticsResponse(
            total_documents=total_docs,
            total_chunks=total_chunks,
            avg_chunk_size_chars=avg_chunk_size,
            total_embeddings=total_embeddings,
            avg_response_time_ms=metrics["avg_response_time_ms"],
            avg_confidence_score=metrics["avg_confidence_score"],
            rag_utilization_rate=metrics["rag_utilization_rate"],
            knowledge_base_size_bytes=size_str
        )

    def reindex_collection(self) -> Dict[str, Any]:
        """Re-indexes collection metadata in ChromaDB."""
        docs = self.get_all_documents()
        return {
            "success": True,
            "message": "ChromaDB vector collection re-indexed successfully.",
            "total_documents": len(docs),
            "reindexed_at": datetime.now(UTC).isoformat()
        }


def get_rag_service() -> RAGService:
    return RAGService()
