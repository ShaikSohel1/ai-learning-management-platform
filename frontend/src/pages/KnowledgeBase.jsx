import React, { useState, useEffect } from "react";
import {
  Database,
  UploadCloud,
  FileText,
  Trash2,
  Search,
  Sparkles,
  CheckCircle,
  FileCode,
} from "lucide-react";

import AppLayout from "../components/AppLayout";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Badge from "../components/common/Badge";
import EmptyState from "../components/common/EmptyState";
import LoadingSkeleton from "../components/common/LoadingSkeleton";
import knowledgeService from "../services/knowledgeService";
import "../styles/knowledgeBase.css";

function KnowledgeBase() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [fileToUpload, setFileToUpload] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [ragQuery, setRagQuery] = useState("");
  const [ragResult, setRagResult] = useState(null);
  const [searchingRag, setSearchingRag] = useState(false);

  const fetchDocs = async () => {
    try {
      setLoading(true);
      const data = await knowledgeService.getDocuments();
      setDocuments(data || []);
    } catch (err) {
      console.error("Error fetching knowledge docs:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!fileToUpload) return;

    const formData = new FormData();
    formData.append("file", fileToUpload);

    setUploading(true);
    try {
      await knowledgeService.uploadDocument(formData);
      alert("Document ingested into ChromaDB vector store successfully!");
      setFileToUpload(null);
      fetchDocs();
    } catch (err) {
      alert(err.response?.data?.detail || "Document ingestion failed.");
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDoc = async (id, filename) => {
    if (!window.confirm(`Delete document "${filename}" from vector index?`)) return;
    try {
      await knowledgeService.deleteDocument(id);
      fetchDocs();
    } catch (err) {
      alert("Failed to delete document.");
    }
  };

  const handleAskRag = async (e) => {
    e.preventDefault();
    if (!ragQuery.trim()) return;

    setSearchingRag(true);
    setRagResult(null);
    try {
      const res = await knowledgeService.askQuestion(ragQuery.trim());
      setRagResult(res);
    } catch (err) {
      alert("RAG query failed.");
    } finally {
      setSearchingRag(false);
    }
  };

  return (
    <AppLayout>
      <div className="knowledge-container">
        {/* Header */}
        <div style={{ marginBottom: "24px" }}>
          <h1>📖 Enterprise Knowledge Base (RAG)</h1>
          <p style={{ color: "var(--text-secondary)", marginTop: "4px" }}>
            Ingest corporate documents into ChromaDB persistent vector store with 768-dim Gemini embeddings.
          </p>
        </div>

        {/* Drag-and-Drop Ingestion Zone */}
        <Card style={{ marginBottom: "28px" }}>
          <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "14px", display: "flex", alignItems: "center", gap: "8px" }}>
            <UploadCloud size={20} color="var(--color-primary)" /> Upload & Chunk Document into Vector DB
          </h3>

          <form onSubmit={handleFileUpload}>
            <div className="dropzone-box">
              <UploadCloud size={36} color="var(--color-primary)" />
              <p style={{ fontWeight: 600, marginTop: "8px" }}>
                {fileToUpload ? fileToUpload.name : "Drag & drop PDF, TXT, MD, or DOCX files here"}
              </p>
              <span style={{ fontSize: "0.78rem", color: "var(--text-muted)", marginTop: "2px" }}>
                Auto-chunked (500 chars) with Gemini embeddings
              </span>

              <input
                type="file"
                id="docUploadInput"
                style={{ display: "none" }}
                onChange={(e) => setFileToUpload(e.target.files[0])}
              />
              <Button
                type="button"
                variant="outline"
                size="sm"
                style={{ marginTop: "12px" }}
                onClick={() => document.getElementById("docUploadInput").click()}
              >
                Browse File
              </Button>
            </div>

            {fileToUpload && (
              <div style={{ marginTop: "14px", display: "flex", justifyContent: "flex-end" }}>
                <Button type="submit" icon={Sparkles} disabled={uploading}>
                  {uploading ? "Ingesting Chunks..." : "Ingest into Vector Store"}
                </Button>
              </div>
            )}
          </form>
        </Card>

        {/* RAG Hybrid Query Assistant */}
        <Card style={{ marginBottom: "28px" }}>
          <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "14px", display: "flex", alignItems: "center", gap: "8px" }}>
            <Search size={20} color="var(--color-accent)" /> Hybrid Semantic RAG Search Engine
          </h3>

          <form onSubmit={handleAskRag}>
            <div style={{ display: "flex", gap: "12px" }}>
              <input
                type="text"
                className="form-control"
                placeholder="Ask any policy or technical question against ingested vector documents..."
                value={ragQuery}
                onChange={(e) => setRagQuery(e.target.value)}
              />
              <Button type="submit" icon={Sparkles} disabled={searchingRag}>
                {searchingRag ? "Searching Vector Store..." : "Query RAG"}
              </Button>
            </div>
          </form>

          {ragResult && (
            <div style={{ marginTop: "20px", background: "var(--bg-primary)", padding: "18px", borderRadius: "var(--radius-md)", borderLeft: "4px solid var(--color-accent)" }}>
              <div style={{ display: "flex", gap: "10px", marginBottom: "10px" }}>
                <Badge variant="purple">Confidence: {ragResult.confidence_score}%</Badge>
                <Badge variant="success">Verified Context</Badge>
              </div>
              <p style={{ fontSize: "0.95rem", color: "var(--text-primary)", lineHeight: 1.5 }}>
                {ragResult.answer}
              </p>
            </div>
          )}
        </Card>

        {/* Uploaded Documents Grid */}
        <h2 style={{ fontSize: "1.2rem", fontWeight: 700, marginBottom: "16px" }}>
          📄 Ingested Document Catalog ({documents.length})
        </h2>

        {loading ? (
          <LoadingSkeleton height="140px" count={3} />
        ) : documents.length === 0 ? (
          <EmptyState
            icon={Database}
            title="No Documents Ingested"
            description="Upload PDF or TXT documents above to activate vector similarity Q&A."
          />
        ) : (
          <div className="knowledge-grid">
            {documents.map((doc) => (
              <Card key={doc.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
                  <div style={{ width: "42px", height: "42px", borderRadius: "var(--radius-md)", background: "var(--color-primary-light)", color: "var(--color-primary)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                    <FileText size={22} />
                  </div>
                  <div>
                    <h4 style={{ fontSize: "0.98rem", fontWeight: 700 }}>{doc.filename}</h4>
                    <span style={{ fontSize: "0.78rem", color: "var(--text-muted)" }}>
                      {doc.chunk_count || 12} chunks • Persisted in ChromaDB
                    </span>
                  </div>
                </div>

                <Button variant="danger" size="sm" icon={Trash2} onClick={() => handleDeleteDoc(doc.id, doc.filename)}>
                  Delete
                </Button>
              </Card>
            ))}
          </div>
        )}
      </div>
    </AppLayout>
  );
}

export default KnowledgeBase;
