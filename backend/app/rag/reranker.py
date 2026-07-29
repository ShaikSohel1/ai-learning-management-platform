"""
Reranker Module.

Implements multi-criteria result reranking for retrieved document chunks.
Combines semantic vector similarity, keyword term overlap frequency, document freshness,
and chunk deduplication to prioritize high-precision context snippets.
"""

import logging
import math

from app.schemas.knowledge import KnowledgeCitation

logger = logging.getLogger(__name__)


class RankedChunk:
    def __init__(
        self,
        citation: KnowledgeCitation,
        final_score: float,
        semantic_score: float,
        keyword_score: float,
        freshness_score: float
    ):
        self.citation = citation
        self.final_score = final_score
        self.semantic_score = semantic_score
        self.keyword_score = keyword_score
        self.freshness_score = freshness_score


class Reranker:
    """Reranks candidate retrieved chunks using weighted multi-criteria scoring."""

    def rerank(
        self,
        citations: list[KnowledgeCitation],
        query_keywords: list[str],
        top_k: int = 4
    ) -> list[RankedChunk]:
        """
        Reranks and deduplicates candidate citations.
        """
        if not citations:
            return []

        ranked_results: list[RankedChunk] = []
        seen_texts = set()

        for cite in citations:
            # Check text deduplication
            normalized_snippet = cite.snippet.strip().lower()
            if normalized_snippet in seen_texts:
                continue
            seen_texts.add(normalized_snippet)

            # 1. Semantic score (0.0 to 1.0)
            sem_score = max(0.0, min(1.0, cite.similarity_score))

            # 2. Keyword overlap score
            kw_score = self._compute_keyword_score(cite.snippet, query_keywords)

            # 3. Freshness score (default baseline 0.8)
            fresh_score = 0.8

            # Combined weighted score
            final_score = (0.55 * sem_score) + (0.35 * kw_score) + (0.10 * fresh_score)
            final_score = round(max(0.0, min(1.0, final_score)), 3)

            # Update citation similarity score to reflect reranked confidence
            cite.similarity_score = final_score

            ranked_results.append(RankedChunk(
                citation=cite,
                final_score=final_score,
                semantic_score=sem_score,
                keyword_score=kw_score,
                freshness_score=fresh_score
            ))

        # Sort by final score descending
        ranked_results.sort(key=lambda r: r.final_score, reverse=True)
        return ranked_results[:top_k]

    def _compute_keyword_score(self, text: str, keywords: list[str]) -> float:
        if not keywords or not text:
            return 0.0

        lower_text = text.lower()
        matched = 0
        for kw in keywords:
            if kw.lower() in lower_text:
                matched += 1

        ratio = matched / len(keywords)
        # Apply non-linear boost for multi-keyword matches
        return math.pow(ratio, 0.7)


reranker = Reranker()
