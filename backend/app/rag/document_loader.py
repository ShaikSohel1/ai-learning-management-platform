"""
Document Loader Module.

Parses and extracts raw text from PDF, TXT, Markdown, and DOCX document formats.
Applies text cleaning and normalization for clean vector chunk generation.
"""

import io
import re
import logging
from typing import Tuple
from pypdf import PdfReader
import docx

logger = logging.getLogger(__name__)


class DocumentLoader:
    """Extracts and normalizes text from multiple document formats."""

    @staticmethod
    def clean_text(text: str) -> str:
        """Removes duplicate whitespace, non-printable artifacts, and normalizes linebreaks."""
        if not text:
            return ""
        # Remove null bytes or weird control chars
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
        # Normalize multiple newlines and spaces
        text = re.sub(r"\r\n|\r", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]{2,}", " ", text)
        return text.strip()

    def load_document(self, filename: str, content_bytes: bytes) -> str:
        """
        Detects file extension and extracts clean text from file bytes.

        Supports: .pdf, .txt, .md, .docx
        """
        ext = filename.lower().split(".")[-1] if "." in filename else ""

        if ext == "pdf":
            raw_text = self._extract_pdf(content_bytes)
        elif ext in ("txt", "md", "markdown"):
            raw_text = self._extract_text(content_bytes)
        elif ext == "docx":
            raw_text = self._extract_docx(content_bytes)
        else:
            # Default text attempt
            raw_text = self._extract_text(content_bytes)

        clean = self.clean_text(raw_text)
        if not clean:
            logger.warning(f"No extractable text found in file '{filename}'")
            return f"Document filename: {filename}\nContent unavailable or binary."
        return clean

    def _extract_pdf(self, content_bytes: bytes) -> str:
        text_parts = []
        try:
            reader = PdfReader(io.BytesIO(content_bytes))
            for idx, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"Error reading PDF content: {e}")
            return ""

    def _extract_text(self, content_bytes: bytes) -> str:
        try:
            return content_bytes.decode("utf-8", errors="replace")
        except Exception as e:
            logger.error(f"Error reading plain text file: {e}")
            return ""

    def _extract_docx(self, content_bytes: bytes) -> str:
        try:
            doc = docx.Document(io.BytesIO(content_bytes))
            text_parts = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"Error reading DOCX content: {e}")
            return ""


document_loader = DocumentLoader()
