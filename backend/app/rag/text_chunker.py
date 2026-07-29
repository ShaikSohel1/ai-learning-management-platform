"""
Text Chunker Module.

Splits long document text into overlapping text chunks to preserve semantic context across chunk boundaries.
"""

from typing import Any


class TextChunk:
    def __init__(self, text: str, index: int, start_char: int, end_char: int):
        self.text = text
        self.index = index
        self.start_char = start_char
        self.end_char = end_char

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "index": self.index,
            "start_char": self.start_char,
            "end_char": self.end_char
        }


class TextChunker:
    """Splits full document text into semantic overlapping chunks."""

    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 60) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> list[TextChunk]:
        """
        Splits text into chunks of maximum size with configured overlap.
        Preserves sentence or paragraph boundaries where possible.
        """
        if not text:
            return []

        chunks: list[TextChunk] = []
        text_length = len(text)
        
        if text_length <= self.chunk_size:
            chunks.append(TextChunk(text=text, index=0, start_char=0, end_char=text_length))
            return chunks

        start = 0
        chunk_idx = 0

        while start < text_length:
            end = start + self.chunk_size

            # If not at the end of the text, attempt to break at sentence/newline boundary
            if end < text_length:
                # Look for paragraph break or sentence end in the last 100 characters of the window
                boundary = max(
                    text.rfind("\n\n", start, end),
                    text.rfind(". ", start, end),
                    text.rfind("\n", start, end)
                )

                if boundary != -1 and boundary > start + (self.chunk_size // 2):
                    end = boundary + 1

            chunk_content = text[start:end].strip()
            if chunk_content:
                chunks.append(TextChunk(
                    text=chunk_content,
                    index=chunk_idx,
                    start_char=start,
                    end_char=end
                ))
                chunk_idx += 1

            start = end - self.chunk_overlap
            if start < 0 or start >= text_length - self.chunk_overlap:
                break

        return chunks


text_chunker = TextChunker()
