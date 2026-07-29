"""
Embedding Service Module.

Generates dense vector embeddings using Google Gemini API via official google-genai SDK (`gemini-embedding-001`).
Implements in-memory embedding caching, batch processing, and offline fallback vector generation.
"""

import hashlib
import logging

from google import genai
from google.genai.errors import APIError

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service generating vector embeddings for text chunks using Gemini gemini-embedding-001."""

    def __init__(self, api_key: str | None = None, model: str = "gemini-embedding-001") -> None:
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = model
        self._cache: dict[str, list[float]] = {}
        self.embedding_dimension = 3072

        if self.api_key and self.api_key != "your_gemini_api_key_here":
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def get_embedding(self, text: str) -> list[float]:
        """
        Fetches embedding vector for single string using google-genai SDK. Uses cache if available.
        """
        text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if text_hash in self._cache:
            return self._cache[text_hash]

        if not self.client:
            vec = self._generate_fallback_vector(text)
            self._cache[text_hash] = vec
            return vec

        try:
            response = self.client.models.embed_content(
                model=self.model,
                contents=text[:2048]
            )
            if response.embeddings and response.embeddings[0].values:
                vec = list(response.embeddings[0].values)
                self._cache[text_hash] = vec
                return vec
            else:
                logger.warning(f"Empty embedding vector returned from Gemini API for model '{self.model}'.")
                vec = self._generate_fallback_vector(text)
                self._cache[text_hash] = vec
                return vec

        except APIError as e:
            logger.error(f"Gemini Embedding APIError [Code {getattr(e, 'code', 'Unknown')}]: {e}")
            vec = self._generate_fallback_vector(text)
            self._cache[text_hash] = vec
            return vec
        except Exception as e:
            logger.error(f"Failed to generate Gemini embedding vector: {e}")
            vec = self._generate_fallback_vector(text)
            self._cache[text_hash] = vec
            return vec

    def get_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generates vector embeddings for a list of text strings.
        """
        return [self.get_embedding(t) for t in texts]

    def _generate_fallback_vector(self, text: str) -> list[float]:
        """
        Generates a deterministic 3072-dimensional normalized float vector from text hash.
        Guarantees offline testing & dev mode without external API failures.
        """
        import math
        vec = []
        seed = int(hashlib.md5(text.encode("utf-8")).hexdigest()[:8], 16)
        for i in range(self.embedding_dimension):
            val = math.sin(seed + i * 0.1)
            vec.append(val)
        
        # L2 normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec


embedding_service = EmbeddingService()
