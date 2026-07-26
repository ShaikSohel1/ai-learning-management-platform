"""
Retriever Module.

Implements Hybrid Search combining vector semantic search, BM25 keyword matching, and metadata filters.
Integrates result reranking and confidence scoring.
"""

import logging
from typing import List, Dict, Any, Tuple, Optional

from app.rag.embedding_service import embedding_service
from app.rag.vector_store import vector_store
from app.rag.query_processor import query_processor, ProcessedQuery
from app.rag.reranker import reranker, RankedChunk
from app.schemas.knowledge import KnowledgeCitation

logger = logging.getLogger(__name__)


class Retriever:
    """Hybrid Retriever combining semantic vector search and keyword term overlap with reranking."""

    def __init__(self) -> None:
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.query_processor = query_processor
        self.reranker = reranker

    def hybrid_search(
        self,
        query: str,
        top_k: int = 4,
        threshold: float = 0.3,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[KnowledgeCitation], float, ProcessedQuery]:
        """
        Executes Hybrid Search Pipeline:
        1. Query Processing (normalization, abbreviation expansion, intent detection).
        2. Vector Similarity Search against ChromaDB.
        3. Multi-Criteria Reranking & Deduplication.
        4. Calculating overall RAG confidence percentage.

        Returns: (citations list, overall_confidence_percent, processed_query_object)
        """
        if not query or not query.strip():
            empty_proc = ProcessedQuery(query, "", "", "general", [], [])
            return [], 0.0, empty_proc

        # Step 1: Query Processor
        proc_query = self.query_processor.process(query)
        logger.info(f"Hybrid search processed query: intent='{proc_query.intent}', optimized='{proc_query.optimized_query}'")

        # Step 2: Vector Search using optimized query text
        query_vector = self.embedding_service.get_embedding(proc_query.optimized_query)
        search_res = self.vector_store.similarity_search(query_embedding=query_vector, top_k=top_k * 3)

        documents_list = search_res.get("documents", [[]])[0]
        metadatas_list = search_res.get("metadatas", [[]])[0]
        distances_list = search_res.get("distances", [[]])[0]

        candidate_citations: List[KnowledgeCitation] = []

        for doc_text, meta, dist in zip(documents_list, metadatas_list, distances_list):
            if not doc_text:
                continue

            # Cosine similarity score = max(0.0, 1.0 - dist)
            sem_similarity = max(0.0, 1.0 - float(dist)) if dist is not None else 0.5
            
            filename = meta.get("filename", "Enterprise Document")
            chunk_idx = meta.get("chunk_index", 0)

            # Metadata filtering check if requested
            if metadata_filter:
                match = True
                for k, v in metadata_filter.items():
                    if meta.get(k) != v:
                        match = False
                        break
                if not match:
                    continue

            candidate_citations.append(KnowledgeCitation(
                document_name=filename,
                chunk_index=chunk_idx,
                similarity_score=round(sem_similarity, 3),
                snippet=doc_text.strip()
            ))

        # Step 3: Multi-Criteria Reranking
        ranked_chunks: List[RankedChunk] = self.reranker.rerank(
            citations=candidate_citations,
            query_keywords=proc_query.keywords,
            top_k=top_k
        )

        final_citations = [rc.citation for rc in ranked_chunks if rc.final_score >= threshold]

        # Step 4: Overall Confidence Scoring
        if final_citations:
            top_score = ranked_chunks[0].final_score
            avg_score = sum(rc.final_score for rc in ranked_chunks[:len(final_citations)]) / len(final_citations)
            overall_confidence = round(((top_score * 0.7) + (avg_score * 0.3)) * 100, 1)
        else:
            overall_confidence = 0.0

        return final_citations, overall_confidence, proc_query


retriever = Retriever()
