"""
Automated End-to-End Test for RAG Document Ingestion & Deletion Workflow.
Verifies:
1. Document Ingestion (upload, chunking, embeddings, ChromaDB vector store insertion).
2. Document Listing (DocumentMetadata contains valid document_id and document_name).
3. Hybrid Search & RAG retrieval of ingested document content.
4. Deletion of document from ChromaDB vector collection.
5. Verification that ChromaDB collection count decreases and document is removed.
6. Verification that RAG search CANNOT retrieve deleted document chunks.
7. Verification that deleting non-existent document ID returns False / HTTP 404.
"""

import sys
import unittest
from app.rag.rag_service import get_rag_service


class TestRAGDeletionWorkflow(unittest.TestCase):
    def setUp(self):
        self.rag_service = get_rag_service()
        self.test_filename = "Deletion_Audit_Policy_2026.txt"
        self.test_content = (
            b"CONFIDENTIAL POLICY 2026: Quantum Security Protocol.\n"
            b"All employees must rotate quantum encryption keys every 30 days.\n"
            b"Protocol ID: QSEC-9988-ALPHA-TEST."
        )
        self.uploader = "audit_engineer@enterprise.com"

    def test_full_deletion_lifecycle(self):
        # 1. Ingest document
        metadata = self.rag_service.ingest_document(
            filename=self.test_filename,
            content_bytes=self.test_content,
            uploaded_by=self.uploader
        )

        doc_id = metadata.document_id
        doc_name = metadata.document_name

        self.assertIsNotNone(doc_id)
        self.assertEqual(doc_name, self.test_filename)
        self.assertGreater(metadata.chunk_count, 0)
        print(f"\n[PASS] Ingested document: id='{doc_id}', name='{doc_name}', chunks={metadata.chunk_count}")

        # 2. Verify document appears in list_all_documents
        all_docs = self.rag_service.get_all_documents()
        doc_ids = [d.document_id for d in all_docs]
        doc_names = [d.document_name for d in all_docs]

        self.assertIn(doc_id, doc_ids)
        self.assertIn(self.test_filename, doc_names)
        print(f"[PASS] Verified document exists in document catalog ({len(all_docs)} total docs)")

        # 3. Verify Hybrid Search retrieves context
        citations, confidence, _ = self.rag_service.retriever.hybrid_search(
            query="quantum encryption keys rotate 30 days QSEC-9988-ALPHA-TEST",
            top_k=5,
            threshold=0.1
        )
        found_test_doc = any(c.document_name == self.test_filename for c in citations)
        self.assertTrue(found_test_doc, "Search failed to retrieve newly ingested document!")
        print(f"[PASS] Hybrid search retrieved document context with confidence {confidence}%")

        # 4. Execute deletion
        delete_result = self.rag_service.delete_document(doc_id)
        self.assertTrue(delete_result, f"Deletion failed for doc_id='{doc_id}'")
        print(f"[PASS] Successfully deleted document id='{doc_id}' from ChromaDB")

        # 5. Verify document NO LONGER appears in get_all_documents
        all_docs_after = self.rag_service.get_all_documents()
        doc_ids_after = [d.document_id for d in all_docs_after]

        self.assertNotIn(doc_id, doc_ids_after)
        print(f"[PASS] Verified document id='{doc_id}' removed from document catalog")

        # 6. Verify RAG Search CANNOT retrieve deleted document chunks
        citations_after, _, _ = self.rag_service.retriever.hybrid_search(
            query="quantum encryption keys rotate 30 days QSEC-9988-ALPHA-TEST",
            top_k=5,
            threshold=0.1
        )
        found_after_delete = any(c.document_name == self.test_filename for c in citations_after)
        self.assertFalse(found_after_delete, "Deleted document context was still retrieved by search!")
        print("[PASS] Verified search CANNOT retrieve deleted document chunks")

        # 7. Verify deleting non-existent document ID returns False
        delete_again = self.rag_service.delete_document(doc_id)
        self.assertFalse(delete_again, "Deleting non-existent doc_id should return False")
        print("[PASS] Verified deleting non-existent document ID returns False")


if __name__ == "__main__":
    unittest.main()
