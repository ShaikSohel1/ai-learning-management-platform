"""
Context Compressor Module.

Extracts sentence-level highlights and key phrases matching query keywords from long text chunks.
Reduces redundant text context before sending to Gemini LLM for prompt token optimization.
"""

import re
import logging
from typing import List
from app.schemas.knowledge import KnowledgeCitation

logger = logging.getLogger(__name__)


class ContextCompressor:
    """Compresses long context chunks into targeted sentence highlights."""

    def compress_citations(
        self,
        citations: List[KnowledgeCitation],
        query_keywords: List[str],
        max_total_chars: int = 2500
    ) -> str:
        """
        Extracts key sentences matching query keywords from each citation.
        Combines them into a compressed context block.
        """
        if not citations:
            return ""

        context_blocks: List[str] = []
        total_chars = 0

        for cite in citations:
            snippet = cite.snippet
            filename = cite.document_name
            chunk_idx = cite.chunk_index

            # Split snippet into sentences
            sentences = re.split(r"(?<=[.!?])\s+", snippet)

            relevant_sentences = []
            for s in sentences:
                s_clean = s.strip()
                if not s_clean:
                    continue

                # Check if sentence contains any query keyword
                if not query_keywords or any(kw.lower() in s_clean.lower() for kw in query_keywords):
                    relevant_sentences.append(s_clean)

            # Fallback to entire snippet if no specific sentence matched
            compressed_text = " ".join(relevant_sentences) if relevant_sentences else snippet

            block = f"[Source: {filename} (Chunk {chunk_idx})]\n{compressed_text}"
            
            if total_chars + len(block) > max_total_chars:
                break

            context_blocks.append(block)
            total_chars += len(block)

        return "\n\n---\n\n".join(context_blocks)


context_compressor = ContextCompressor()
