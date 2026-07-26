"""
Vector Store Module.

Encapsulates persistent ChromaDB vector store operations.
Manages document embeddings, chunk metadata, similarity vector queries, and document deletion.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

logger = logging.getLogger(__name__)


class VectorStore:
    """Manages persistent vector collection storage using ChromaDB."""

    def __init__(self, persist_dir: str = "./chroma_db", collection_name: str = "enterprise_knowledge") -> None:
        self.persist_dir = os.path.abspath(persist_dir)
        os.makedirs(self.persist_dir, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"Initialized ChromaDB vector store at '{self.persist_dir}', collection='{self.collection_name}'")

    def add_chunks(
        self,
        doc_id: str,
        filename: str,
        uploader: str,
        upload_date: str,
        chunks: List[str],
        embeddings: List[List[float]]
    ) -> int:
        """
        Stores vector embeddings, text chunks, and metadata into ChromaDB collection.
        """
        if not chunks or not embeddings:
            return 0

        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "doc_id": doc_id,
                "filename": filename,
                "uploader": uploader,
                "upload_date": upload_date,
                "chunk_index": i,
            }
            for i in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )
        logger.info(f"Added {len(chunks)} chunks to ChromaDB for doc_id='{doc_id}' ({filename})")
        return len(chunks)

    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 4
    ) -> Dict[str, Any]:
        """
        Performs vector similarity search in ChromaDB using query embedding.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        return results

    def delete_document(self, doc_id: str) -> bool:
        """
        Deletes all chunks belonging to a document from ChromaDB vector collection.
        """
        try:
            self.collection.delete(where={"doc_id": doc_id})
            logger.info(f"Deleted vector entries for doc_id='{doc_id}' from ChromaDB")
            return True
        except Exception as e:
            logger.error(f"Error deleting doc_id='{doc_id}' from ChromaDB: {e}")
            return False

    def list_all_metadatas(self) -> List[Dict[str, Any]]:
        """
        Retrieves all chunk metadatas to compile document summary catalog.
        """
        try:
            res = self.collection.get(include=["metadatas"])
            return res.get("metadatas", []) or []
        except Exception as e:
            logger.error(f"Failed to fetch metadatas from ChromaDB: {e}")
            return []


vector_store = VectorStore()
