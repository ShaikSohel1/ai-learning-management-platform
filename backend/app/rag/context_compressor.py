"""
Context Compressor Module.

Extracts sentence-level highlights and key phrases matching query keywords from long text chunks.
Reduces redundant text context before sending to Gemini LLM for prompt token optimization.
Includes abbreviation-aware NLP sentence boundary detection (protecting Mr., Dr., Inc., U.S., etc.).
"""

import logging
import re

from app.schemas.knowledge import KnowledgeCitation

logger = logging.getLogger(__name__)

COMMON_ABBREVIATIONS = {
    "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "rev", "st", "gov", "sen", "rep",
    "inc", "ltd", "co", "corp", "llc", "u.s", "u.k", "u.s.a", "e.g", "i.e", "etc",
    "vs", "v", "approx", "dept", "est", "min", "max", "fig", "no", "vol"
}


class ContextCompressor:
    """Compresses long context chunks into targeted sentence highlights with abbreviation-aware NLP sentence splitting."""

    def _split_sentences(self, text: str) -> list[str]:
        """
        Splits text into sentences while respecting common abbreviations, acronyms, and honorifics.
        Prevents false sentence boundaries at titles like 'Mr.', 'Dr.', 'Inc.', 'U.S.', etc.
        """
        if not text:
            return []

        pattern = re.compile(r"([.!?]+)(\s+|\n+)")
        sentences = []
        current_start = 0

        for match in pattern.finditer(text):
            punct = match.group(1)
            space_end = match.end(2)

            pre_text = text[current_start:match.start(1)].rstrip()
            words = pre_text.split()
            last_word = words[-1].lower() if words else ""
            clean_last_word = re.sub(r"^\W+|\W+$", "", last_word)

            next_char = text[space_end:space_end + 1]

            is_abbrev = clean_last_word in COMMON_ABBREVIATIONS or last_word in COMMON_ABBREVIATIONS
            is_single_initial = len(clean_last_word) == 1 and clean_last_word.isalpha()
            is_next_lowercase = next_char.islower() if next_char else False

            if (punct == "." and (is_abbrev or is_single_initial)) or is_next_lowercase:
                continue

            sentence = text[current_start:space_end].strip()
            if sentence:
                sentences.append(sentence)
            current_start = space_end

        remaining = text[current_start:].strip()
        if remaining:
            sentences.append(remaining)

        return sentences

    def compress_citations(
        self,
        citations: list[KnowledgeCitation],
        query_keywords: list[str],
        max_total_chars: int = 2500
    ) -> str:
        """
        Extracts key sentences matching query keywords from each citation.
        Combines them into a compressed context block.
        """
        if not citations:
            return ""

        context_blocks: list[str] = []
        total_chars = 0

        for cite in citations:
            snippet = cite.snippet
            filename = cite.document_name
            chunk_idx = cite.chunk_index

            # Split snippet into sentences using abbreviation-aware sentence boundary detection
            sentences = self._split_sentences(snippet)

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
