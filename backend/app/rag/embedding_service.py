"""
Embedding Service Module.

Generates dense vector embeddings using Google Gemini API (`text-embedding-004`).
Implements in-memory embedding caching, batch processing, and offline fallback vector generation.
"""

import hashlib
import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service generating vector embeddings for text chunks using Gemini text-embedding-004."""

    def __init__(self, api_key: str | None = None, model: str = "text-embedding-004") -> None:
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self._cache: dict[str, list[float]] = {}
        self.embedding_dimension = 768

    def get_embedding(self, text: str) -> list[float]:
        """
        Fetches embedding vector for single string. Uses cache if available.
        """
        text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if text_hash in self._cache:
            return self._cache[text_hash]

        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            vec = self._generate_fallback_vector(text)
            self._cache[text_hash] = vec
            return vec

        endpoint = f"{self.base_url}/{self.model}:embedContent?key={self.api_key}"
        payload = {
            "model": f"models/{self.model}",
            "content": {"parts": [{"text": text[:2048]}]}
        }

        try:
            with httpx.Client(timeout=20.0) as client:
                response = client.post(endpoint, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    vec = data["embedding"]["values"]
                    self._cache[text_hash] = vec
                    return vec
                else:
                    logger.error(f"Embedding API error HTTP {response.status_code}: {response.text}")
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
        Generates a deterministic 768-dimensional normalized float vector from text hash.
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
