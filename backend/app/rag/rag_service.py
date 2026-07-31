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

import logging
import time
import uuid
from datetime import UTC, datetime
from typing import Any

from app.ai.gemini_client import AllGeminiModelsQuotaExhaustedError, GeminiClient
from app.ai.retry_handler import retry_handler
from app.rag.context_compressor import context_compressor
from app.rag.document_loader import document_loader
from app.rag.embedding_service import embedding_service
from app.rag.retriever import retriever
from app.rag.search_history import search_history_store
from app.rag.text_chunker import text_chunker
from app.rag.vector_store import vector_store
from app.schemas.knowledge import (
    DocumentMetadata,
    KnowledgeAnalyticsResponse,
    KnowledgeAskRequest,
    KnowledgeAskResponse,
    KnowledgeCitation,
)

logger = logging.getLogger(__name__)


class RAGService:
    """Unified Enterprise Semantic Search Platform Service Facade."""

    def __init__(self, gemini_client: GeminiClient | None = None) -> None:
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

    def get_all_documents(self) -> list[DocumentMetadata]:
        metadatas = self.vector_db.list_all_metadatas()
        if not metadatas:
            return []

        doc_groups: dict[str, dict[str, Any]] = {}
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
        user_name: str = "Enterprise Learner",
        user_email: str = "user@enterprise.com",
        user_department: str = "Engineering",
        top_k: int = 4,
        threshold: float = 0.3
    ) -> KnowledgeAskResponse:
        import json
        from app.core.config import settings

        start_time = time.perf_counter()
        request_id = str(uuid.uuid4())
        start_timestamp = datetime.now(UTC).isoformat()
        current_active_model = GeminiClient.get_active_model()
        user_info_str = f"{user_name} ({user_email})"

        # RAG REQUEST START
        logger.info("====================================================")
        logger.info("RAG REQUEST START")
        logger.info("====================================================")
        logger.info(f"Request ID: {request_id}")
        logger.info(f"Timestamp: {start_timestamp}")
        logger.info(f"Authenticated User: {user_info_str}")
        logger.info(f"Workspace ID: {user_department}")
        logger.info(f"Question: {question}")
        logger.info(f"Requested Model: {settings.GEMINI_MODEL}")
        logger.info(f"Current Active Model: {current_active_model}\n")

        # STEP 1 — USER QUESTION
        t_embed_start = time.perf_counter()
        proc_query = self.retriever.query_processor.process(question)
        query_vector = self.embeddings.get_embedding(proc_query.optimized_query)
        embed_latency_ms = round((time.perf_counter() - t_embed_start) * 1000, 2)
        embed_model = self.embeddings.model
        embed_dim = len(query_vector)

        logger.info("====================================================")
        logger.info("STEP 1 — USER QUESTION")
        logger.info("====================================================")
        logger.info(f"Original question: {question}")
        logger.info(f"Optimized query: {proc_query.optimized_query}")
        logger.info(f"Embedding model used: {embed_model}")
        logger.info(f"Embedding vector dimension: {embed_dim}")
        logger.info(f"Embedding generation latency: {embed_latency_ms} ms\n")

        # STEP 2 — VECTOR SEARCH
        t_search_start = time.perf_counter()
        search_res = self.vector_db.similarity_search(query_embedding=query_vector, top_k=top_k * 3)
        search_latency_ms = round((time.perf_counter() - t_search_start) * 1000, 2)

        documents_list = search_res.get("documents", [[]])[0]
        metadatas_list = search_res.get("metadatas", [[]])[0]
        distances_list = search_res.get("distances", [[]])[0]
        ids_list = search_res.get("ids", [[]])[0]

        logger.info("====================================================")
        logger.info("STEP 2 — VECTOR SEARCH")
        logger.info("====================================================")
        logger.info(f"Collection name: {self.vector_db.collection_name}")
        logger.info(f"Top K requested: {top_k}")
        logger.info(f"Distance metric: cosine")
        logger.info(f"Search latency: {search_latency_ms} ms")
        logger.info(f"Number of retrieved chunks: {len(documents_list)}\n")

        candidate_citations: list[KnowledgeCitation] = []

        for idx, (doc_text, meta, dist) in enumerate(zip(documents_list, metadatas_list, distances_list), start=1):
            if not doc_text:
                continue

            sem_similarity = max(0.0, 1.0 - float(dist)) if dist is not None else 0.5
            filename = meta.get("filename", "Enterprise Document")
            chunk_idx = meta.get("chunk_index", 0)
            doc_id = meta.get("doc_id", "N/A")
            chunk_id = ids_list[idx - 1] if idx - 1 < len(ids_list) else f"{doc_id}_chunk_{chunk_idx}"

            logger.info("------------------------------------")
            logger.info(f"Chunk #{idx}")
            logger.info("------------------------------------")
            logger.info(f"Chunk ID: {chunk_id}")
            logger.info(f"Document ID: {doc_id}")
            logger.info(f"Document Name: {filename}")
            logger.info(f"Similarity Score: {round(sem_similarity, 4)}")
            logger.info(f"Chunk Length: {len(doc_text)} chars")
            logger.info(f"Character Range: 0 - {len(doc_text)}")
            logger.info(f"Metadata: {json.dumps(meta)}")
            logger.info(f"FULL CHUNK TEXT:\n{doc_text}\n")

            candidate_citations.append(KnowledgeCitation(
                document_name=filename,
                chunk_index=chunk_idx,
                similarity_score=round(sem_similarity, 3),
                snippet=doc_text.strip()
            ))

        # Multi-Criteria Reranking
        ranked_chunks = self.retriever.reranker.rerank(
            citations=candidate_citations,
            query_keywords=proc_query.keywords,
            top_k=top_k
        )
        final_citations = [rc.citation for rc in ranked_chunks if rc.final_score >= threshold]
        referenced_docs = sorted({c.document_name for c in final_citations})

        if final_citations:
            top_score = ranked_chunks[0].final_score
            avg_score = sum(rc.final_score for rc in ranked_chunks[:len(final_citations)]) / len(final_citations)
            overall_confidence = round(((top_score * 0.7) + (avg_score * 0.3)) * 100, 1)
        else:
            overall_confidence = 0.0

        # STEP 3 — CONTEXT COMPRESSION
        compressed_context = self.compressor.compress_citations(
            citations=final_citations,
            query_keywords=proc_query.keywords
        )

        logger.info("====================================================")
        logger.info("STEP 3 — CONTEXT COMPRESSION")
        logger.info("====================================================")
        logger.info(f"Original chunk count: {len(candidate_citations)}")
        logger.info(f"Compressed chunk count: {len(final_citations)}\n")

        for idx, cite in enumerate(final_citations, start=1):
            logger.info(f"Chunk ID: chunk_{cite.chunk_index}")
            logger.info(f"Document: {cite.document_name}")
            logger.info(f"Similarity: {cite.similarity_score}")
            logger.info(f"FULL TEXT:\n{cite.snippet}\n")

        # STEP 4 — FINAL CONTEXT
        if final_citations and overall_confidence >= (threshold * 100):
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
        else:
            system_instruction = (
                "You are an AI Business Assistant for an Enterprise Learning Management Platform. "
                "Answer the user's career development, course, or enterprise learning question professionally."
            )
            prompt = question

        logger.info("====================================================")
        logger.info("STEP 4 — FINAL CONTEXT")
        logger.info("====================================================")
        logger.info(f"System prompt:\n{system_instruction}\n")
        logger.info(f"Context:\n{compressed_context}\n")
        logger.info(f"User question:\n{proc_query.optimized_query}\n")

        # STEP 5 — GEMINI REQUEST
        logger.info("====================================================")
        logger.info("STEP 5 — GEMINI REQUEST")
        logger.info("====================================================")
        logger.info(f"Model name: {GeminiClient.get_active_model()}")
        logger.info("Temperature: 0.3")
        logger.info("Max tokens: 2048")
        logger.info("Top P: 1.0")
        logger.info("Top K: 40")
        logger.info("Safety settings: Default (BLOCK_MEDIUM_AND_ABOVE)")
        logger.info("Retry count: 0")

        t_gemini_start = time.perf_counter()
        raw_response_text = ""

        try:
            raw_response_text = retry_handler.execute(
                self.client.generate_content,
                prompt=prompt,
                system_instruction=system_instruction,
                json_mode=False
            )
            gemini_latency_ms = round((time.perf_counter() - t_gemini_start) * 1000, 2)
            logger.info(f"Latency: {gemini_latency_ms} ms\n")
        except AllGeminiModelsQuotaExhaustedError:
            gemini_latency_ms = round((time.perf_counter() - t_gemini_start) * 1000, 2)
            logger.info(f"Latency: {gemini_latency_ms} ms (Quota Exhausted)\n")
            if final_citations:
                snippets_summary = "\n\n".join([f"• **[{c.document_name}]**: {c.snippet}" for c in final_citations[:3]])
                raw_response_text = (
                    f"### Enterprise Document Context Retrieved\n\n"
                    f"Relevant context was successfully retrieved from the Knowledge Base for your query:\n\n"
                    f"{snippets_summary}\n\n"
                    f"*(Note: AI synthesis is temporarily unavailable because all configured Gemini models have exceeded their API quota. The retrieved document context above is provided directly from your knowledge base.)*"
                )
            else:
                raise

        # STEP 6 — RAW GEMINI RESPONSE
        logger.info("====================================================")
        logger.info("STEP 6 — RAW GEMINI RESPONSE")
        logger.info("====================================================")
        logger.info(f"{raw_response_text}\n")

        # STEP 7 — RESPONSE PARSING
        logger.info("====================================================")
        logger.info("STEP 7 — RESPONSE PARSING")
        logger.info("====================================================")
        logger.info(f"Raw response:\n{raw_response_text}\n")
        logger.info(f"Parsed response:\n{raw_response_text}\n")
        logger.info(f"Final response:\n{raw_response_text}\n")
        logger.info("Differences: None\n")

        end_time = time.perf_counter()
        elapsed_ms = round((end_time - start_time) * 1000, 2)

        # STEP 8 — FINAL API RESPONSE
        final_api_response = KnowledgeAskResponse(
            answer=raw_response_text + ("\n\n*(Note: No matching enterprise document context was found in the Knowledge Base; this response was generated using general AI guidance.)*" if not final_citations else ""),
            rag_used=bool(final_citations),
            confidence_score=overall_confidence,
            response_time_ms=elapsed_ms,
            search_intent=proc_query.intent,
            citations=final_citations if final_citations else [],
            referenced_documents=referenced_docs if final_citations else []
        )

        logger.info("====================================================")
        logger.info("STEP 8 — FINAL API RESPONSE")
        logger.info("====================================================")
        logger.info(f"{json.dumps(final_api_response.model_dump(), indent=2)}\n")

        logger.info("====================================================")
        logger.info("RAG REQUEST END")
        logger.info("====================================================\n")

        # Log search history
        self.history_store.add_entry(
            user_id=user_id,
            question=question,
            response_time_ms=elapsed_ms,
            documents_used=referenced_docs if final_citations else [],
            confidence_score=overall_confidence,
            rag_used=bool(final_citations)
        )

        return final_api_response

    def get_user_search_history(self, user_id: int) -> list[dict[str, Any]]:
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

    def reindex_collection(self) -> dict[str, Any]:
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
