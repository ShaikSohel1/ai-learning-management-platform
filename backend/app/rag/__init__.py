"""
Retrieval Augmented Generation (RAG) Architecture Package.

Components:
- document_loader: Extracts raw text from PDF, TXT, Markdown, and DOCX files.
- text_chunker: Splits text into overlapping semantic chunks.
- embedding_service: Generates Google Gemini vector embeddings (text-embedding-004) with caching & batching.
- vector_store: Manages persistent ChromaDB vector collections, metadata, and deletion.
- retriever: Queries vector store, filters by threshold, ranks context, and builds citations.
- rag_service: Unified business facade for document ingestion, retrieval QA, and Gemini fallback.
"""

from app.rag.rag_service import RAGService, get_rag_service

__all__ = ["RAGService", "get_rag_service"]
