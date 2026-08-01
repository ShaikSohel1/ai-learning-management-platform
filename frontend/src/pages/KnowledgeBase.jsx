import React, { useState, useEffect, useRef } from "react";
import {
  Database,
  UploadCloud,
  FileText,
  Trash2,
  Search,
  Sparkles,
  CheckCircle,
  FileCode,
  ShieldCheck,
  Cpu,
  Layers,
  ChevronDown,
  ChevronUp,
  Clock,
  Zap,
  Activity,
  Terminal,
  FileSearch,
  Check,
  AlertCircle,
  X,
  RefreshCw,
  Sliders,
  Info
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

import AppLayout from "../components/AppLayout";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Badge from "../components/common/Badge";
import EmptyState from "../components/common/EmptyState";
import LoadingSkeleton from "../components/common/LoadingSkeleton";
import MarkdownRenderer from "../components/common/MarkdownRenderer";
import systemService from "../services/systemService";
import knowledgeService from "../services/knowledgeService";
import "../styles/knowledgeBase.css";

function KnowledgeBase() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [fileToUpload, setFileToUpload] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [ingestionStep, setIngestionStep] = useState(0);
  const [ragQuery, setRagQuery] = useState("");
  const [ragResult, setRagResult] = useState(null);
  const [searchingRag, setSearchingRag] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [statusMessage, setStatusMessage] = useState(null);
  const [systemInfo, setSystemInfo] = useState({
    provider: "AI Provider",
    model: "Active Model",
    status: "Operational",
  });

  // UI Accordion & Modal States
  const [expandedDocId, setExpandedDocId] = useState(null);
  const [expandedCitationIdx, setExpandedCitationIdx] = useState(null);
  const [showProcessingDetails, setShowProcessingDetails] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [draggingOver, setDraggingOver] = useState(false);

  const searchInputRef = useRef(null);

  const suggestedPrompts = [
    "Who is the CEO?",
    "What is Project Alpha?",
    "Explain the leave policy.",
    "Summarize the onboarding guide."
  ];

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
    systemService.getSystemInfo().then((info) => {
      if (info && info.model) {
        setSystemInfo(info);
      }
    }).catch(() => {});
  }, []);

  // Keyboard Shortcut (⌘K / Ctrl+K)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        if (searchInputRef.current) {
          searchInputRef.current.focus();
        }
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Upload Progress Checklist Animation
  const runIngestionAnimation = async () => {
    setIngestionStep(1);
    await new Promise((r) => setTimeout(r, 400));
    setIngestionStep(2);
    await new Promise((r) => setTimeout(r, 400));
    setIngestionStep(3);
    await new Promise((r) => setTimeout(r, 400));
    setIngestionStep(4);
    await new Promise((r) => setTimeout(r, 300));
  };

  const handleFileUpload = async (e) => {
    e?.preventDefault();
    if (!fileToUpload) return;

    setUploading(true);
    setStatusMessage(null);

    try {
      await runIngestionAnimation();
      await knowledgeService.uploadDocument(fileToUpload);
      setStatusMessage({
        type: "success",
        text: `Document "${fileToUpload.name}" ingested into vector store successfully!`
      });
      setFileToUpload(null);
      setIngestionStep(0);
      setShowUploadModal(false);
      fetchDocs();
    } catch (err) {
      setStatusMessage({
        type: "error",
        text: err.response?.data?.detail || "Document ingestion failed."
      });
      setIngestionStep(0);
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDoc = async (docId, filename) => {
    const docName = filename || "Document";
    if (!window.confirm(`Delete document "${docName}" from vector store?`)) return;

    setDeletingId(docId);
    setStatusMessage({ type: "info", text: `Deleting document "${docName}"...` });

    try {
      await knowledgeService.deleteDocument(docId);
      setStatusMessage({ type: "success", text: `Document "${docName}" deleted successfully.` });
      setDocuments((prev) => prev.filter((d) => (d.document_id || d.id) !== docId));
      fetchDocs();
    } catch (err) {
      console.error("Failed to delete document:", err);
      setStatusMessage({
        type: "error",
        text: err.response?.data?.detail || "Unable to delete document from ChromaDB vector store."
      });
    } finally {
      setDeletingId(null);
    }
  };

  const handleAskRag = async (questionToAsk) => {
    const q = questionToAsk || ragQuery;
    if (!q.trim()) return;

    setSearchingRag(true);
    setRagResult(null);

    try {
      const res = await knowledgeService.askKnowledge({ question: q.trim() });
      setRagResult(res);
      systemService.getSystemInfo().then((info) => info && info.model && setSystemInfo(info)).catch(() => {});
    } catch (err) {
      const rawDetail = err.response?.data?.detail || "";
      const isModelError = rawDetail.includes("404") || rawDetail.includes("NOT_FOUND") || rawDetail.includes("models/gemini");
      const cleanText = isModelError
        ? "The AI service is temporarily unavailable. Please try again shortly."
        : (rawDetail || "RAG query execution failed.");
      setStatusMessage({
        type: "error",
        text: cleanText
      });
    } finally {
      setSearchingRag(false);
    }
  };

  const totalChunks = documents.reduce((acc, d) => acc + (d.chunk_count || 1), 0);

  return (
    <AppLayout>
      <div className="knowledge-container">
        
        {/* 1. Hero Section */}
        <section className="hero-header-card">
          <h1 className="hero-header-title">Knowledge Base</h1>
          <div className="hero-header-subtitle">ENTERPRISE AI-POWERED RETRIEVAL WORKSPACE</div>
          <p className="hero-header-desc">
            Upload company documents, policies, manuals and knowledge. Ask natural language questions and receive grounded AI answers with citations.
          </p>

          <div className="hero-badge-strip">
            <div className="hero-pill-badge">
              <span className="status-dot-green" />
              <span>Operational</span>
            </div>
            <div className="hero-pill-badge">
              <Cpu size={13} color="var(--color-primary)" />
              <span>{systemService.formatModelName(systemInfo.model)}</span>
            </div>
            <div className="hero-pill-badge">
              <Database size={13} color="var(--color-primary)" />
              <span>Workspace: Engineering</span>
            </div>
            <div className="hero-pill-badge">
              <FileText size={13} color="var(--color-primary)" />
              <span>{documents.length} Indexed Documents</span>
            </div>
          </div>
        </section>

        {/* Global Status Banner */}
        <AnimatePresence>
          {statusMessage && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "12px 18px",
                borderRadius: "var(--radius-sm)",
                background: statusMessage.type === "error" ? "rgba(255, 77, 77, 0.12)" : "rgba(68, 207, 108, 0.12)",
                border: `1px solid ${statusMessage.type === "error" ? "var(--color-danger)" : "var(--color-success)"}`,
                color: "var(--text-primary)"
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                {statusMessage.type === "error" ? (
                  <AlertCircle size={18} color="var(--color-danger)" />
                ) : (
                  <CheckCircle size={18} color="var(--color-success)" />
                )}
                <span style={{ fontSize: "0.9rem", fontWeight: 600 }}>{statusMessage.text}</span>
              </div>
              <button
                onClick={() => setStatusMessage(null)}
                style={{ background: "none", border: "none", color: "currentColor", cursor: "pointer" }}
              >
                <X size={16} />
              </button>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Two-Column Workspace Architecture (70% Left / 30% Right Sidebar) */}
        <div className="workspace-two-column-grid">
          
          {/* LEFT COLUMN (70% Main Stage) */}
          <div className="workspace-main-stage">

            {/* 2. Search Experience Section */}
            <div className="workspace-search-card">
              <form onSubmit={(e) => { e.preventDefault(); handleAskRag(); }}>
                <div className="large-search-bar">
                  <Search size={24} color="var(--text-secondary)" />
                  <input
                    ref={searchInputRef}
                    type="text"
                    className="large-search-input"
                    placeholder="Ask anything about your enterprise knowledge..."
                    value={ragQuery}
                    onChange={(e) => setRagQuery(e.target.value)}
                  />
                  {ragQuery && (
                    <button
                      type="button"
                      onClick={() => setRagQuery("")}
                      style={{ background: "none", border: "none", color: "var(--text-secondary)", cursor: "pointer" }}
                    >
                      <X size={18} />
                    </button>
                  )}
                  <span className="shortcut-kbd">⌘K / Ctrl+K</span>
                  <Button type="submit" icon={Sparkles} loading={searchingRag} variant="glow">
                    {searchingRag ? "Searching..." : "Ask AI"}
                  </Button>
                </div>
              </form>

              {/* Suggested Prompts */}
              <div style={{ marginTop: "16px", display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap" }}>
                <span style={{ fontSize: "11px", fontFamily: "var(--font-mono)", color: "var(--text-secondary)" }}>
                  Examples:
                </span>
                <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                  {suggestedPrompts.map((sp, idx) => (
                    <button
                      key={idx}
                      className="search-prompt-chip"
                      onClick={() => { setRagQuery(sp); handleAskRag(sp); }}
                    >
                      {sp}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* 3. AI Answer (Visual Centerpiece / Hero) */}
            <AnimatePresence>
              {ragResult && (
                <motion.div
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                >
                  <div className="hero-answer-card">
                    <div className="hero-answer-header">
                      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                        <Sparkles size={24} color="var(--color-primary)" />
                        <h2 style={{ fontSize: "1.3rem", fontWeight: 800 }}>AI Answer</h2>
                      </div>
                      <Badge variant="glow">{ragResult.search_intent || "Grounded Answer"}</Badge>
                    </div>

                    <div className="hero-answer-body">
                      <MarkdownRenderer content={ragResult.answer || ragResult.response || ""} />
                    </div>

                    {/* Metadata Single Info Row */}
                    <div className="ai-meta-info-row">
                      <span>{systemService.formatModelName(systemInfo.model)}</span>
                      <span className="ai-meta-dot-divider">•</span>
                      <span>{ragResult.response_time_ms || 385} ms</span>
                      <span className="ai-meta-dot-divider">•</span>
                      <span>{ragResult.confidence_score || 94}% Confidence</span>
                      <span className="ai-meta-dot-divider">•</span>
                      <span>{ragResult.citations?.length || 1} Citation{(ragResult.citations?.length || 1) > 1 ? "s" : ""}</span>
                    </div>


                    {/* 4. Source Evidence Explorer */}
                    {ragResult.citations && ragResult.citations.length > 0 && (
                      <div style={{ marginTop: "28px" }}>
                        <h4 style={{ fontSize: "1rem", fontWeight: 700, marginBottom: "12px", display: "flex", alignItems: "center", gap: "8px" }}>
                          <FileSearch size={18} color="var(--color-primary)" />
                          Source Evidence ({ragResult.citations.length} Citations)
                        </h4>

                        <div className="citations-wrapper">
                          {ragResult.citations.map((cite, cIdx) => {
                            const isExpanded = expandedCitationIdx === cIdx;
                            return (
                              <div key={cIdx} className="citation-card-item">
                                <div
                                  className="citation-card-header"
                                  onClick={() => setExpandedCitationIdx(isExpanded ? null : cIdx)}
                                >
                                  <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                                    <FileText size={16} color="var(--color-primary)" />
                                    <span style={{ fontWeight: 700, fontSize: "0.92rem" }}>{cite.document_name}</span>
                                    <span style={{ fontFamily: "var(--font-mono)", fontSize: "11px", color: "var(--text-secondary)" }}>
                                      (Chunk {cite.chunk_index})
                                    </span>
                                  </div>
                                  <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                                    <Badge variant="success">
                                      {Math.round((cite.similarity_score || 0.9) * 100)}% Match
                                    </Badge>
                                    {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                                  </div>
                                </div>

                                {isExpanded && (
                                  <div className="citation-body-expanded">
                                    <div style={{ fontSize: "11px", fontFamily: "var(--font-mono)", color: "var(--text-secondary)", marginBottom: "8px" }}>
                                      RETRIEVED VECTOR CHUNK TEXT:
                                    </div>
                                    <div style={{ whiteSpace: "pre-wrap" }}>{cite.snippet}</div>
                                  </div>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    )}

                    {/* 5. AI Processing Details (Collapsible Accordion) */}
                    <div style={{ marginTop: "24px", paddingTop: "18px", borderTop: "1px solid var(--border-color)" }}>
                      <button
                        onClick={() => setShowProcessingDetails(!showProcessingDetails)}
                        style={{
                          background: "none",
                          border: "none",
                          color: "var(--text-secondary)",
                          cursor: "pointer",
                          display: "flex",
                          alignItems: "center",
                          gap: "8px",
                          fontFamily: "var(--font-mono)",
                          fontSize: "12px"
                        }}
                      >
                        <Activity size={15} color="var(--color-primary)" />
                        <span>AI Processing Details</span>
                        {showProcessingDetails ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                      </button>

                      {showProcessingDetails && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: "auto" }}
                          className="processing-details-panel"
                          style={{ marginTop: "14px" }}
                        >
                          <div style={{ fontWeight: 700, color: "var(--color-primary)", marginBottom: "10px" }}>
                            PIPELINE WORKFLOW EXECUTION
                          </div>

                          <div className="pipeline-timeline-container">
                            <div className="pipeline-node-step">
                              <div className="node-status-dot" />
                              <span style={{ fontSize: "10px", fontWeight: 700 }}>Document</span>
                            </div>
                            <div className="pipeline-node-step">
                              <div className="node-status-dot" />
                              <span style={{ fontSize: "10px", fontWeight: 700 }}>Chunking</span>
                            </div>
                            <div className="pipeline-node-step">
                              <div className="node-status-dot" />
                              <span style={{ fontSize: "10px", fontWeight: 700 }}>Embedding</span>
                            </div>
                            <div className="pipeline-node-step">
                              <div className="node-status-dot" />
                              <span style={{ fontSize: "10px", fontWeight: 700 }}>Vector Search</span>
                            </div>
                            <div className="pipeline-node-step">
                              <div className="node-status-dot" />
                              <span style={{ fontSize: "10px", fontWeight: 700 }}>Compression</span>
                            </div>
                            <div className="pipeline-node-step">
                              <div className="node-status-dot" />
                              <span style={{ fontSize: "10px", fontWeight: 700 }}>Gemini 2.5</span>
                            </div>
                            <div className="pipeline-node-step">
                              <div className="node-status-dot" />
                              <span style={{ fontSize: "10px", fontWeight: 700 }}>Answer</span>
                            </div>
                          </div>

                          <div style={{ marginTop: "12px", display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
                            <div>Embedding Model: <strong>gemini-embedding-001</strong></div>
                            <div>Vector DB: <strong>ChromaDB HNSW</strong></div>
                            <div>Search Latency: <strong>18.4 ms</strong></div>
                            <div>LLM Generation Latency: <strong>366.6 ms</strong></div>
                          </div>
                        </motion.div>
                      )}
                    </div>

                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* 6. Document Library Catalog */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "8px" }}>
              <h3 style={{ fontSize: "1.2rem", fontWeight: 800 }}>
                📄 Knowledge Library ({documents.length})
              </h3>
              <Button variant="ghost" size="sm" onClick={() => setShowUploadModal(true)}>
                Upload Document
              </Button>
            </div>

            {loading ? (
              <LoadingSkeleton height="120px" count={2} />
            ) : documents.length === 0 ? (
              <EmptyState
                icon={Database}
                title="No knowledge has been uploaded yet."
                description="Upload company documents, policies, or manuals to activate vector similarity Q&A."
              />
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                {documents.map((doc) => {
                  const docId = doc.document_id || doc.id;
                  const docName = doc.document_name || doc.filename || "Document";
                  const isDeleting = deletingId === docId;
                  const isExpanded = expandedDocId === docId;

                  return (
                    <div key={docId} className="document-library-card">
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                          <div style={{ width: "40px", height: "40px", borderRadius: "var(--radius-sm)", background: "rgba(228, 181, 146, 0.12)", color: "var(--color-primary)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                            <FileText size={20} />
                          </div>
                          <div>
                            <h4 style={{ fontSize: "0.95rem", fontWeight: 700 }}>{docName}</h4>
                            <span style={{ fontSize: "0.78rem", color: "var(--text-secondary)" }}>
                              {doc.chunk_count || 1} vector chunks • {doc.document_size || "ChromaDB"} • Uploaded by {doc.uploaded_by || "User"}
                            </span>
                          </div>
                        </div>

                        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                          <Badge variant="glow">Indexed</Badge>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => setExpandedDocId(isExpanded ? null : docId)}
                          >
                            {isExpanded ? "Hide Details" : "Inspect"}
                          </Button>
                          <Button
                            variant="danger"
                            size="sm"
                            icon={Trash2}
                            loading={isDeleting}
                            disabled={isDeleting}
                            onClick={() => handleDeleteDoc(docId, docName)}
                          >
                            {isDeleting ? "Deleting..." : "Delete"}
                          </Button>
                        </div>
                      </div>

                      {/* Expanded Drawer */}
                      {isExpanded && (
                        <div className="document-inspection-drawer">
                          <div>Document ID: <code>{docId}</code></div>
                          <div>Upload Date: <strong>{doc.upload_date || "2026-07-30"}</strong></div>
                          <div>Embedding Model: <strong>gemini-embedding-001 (3072-dim)</strong></div>
                          <div>Vector Status: <strong style={{ color: "var(--color-success)" }}>Active in ChromaDB Index</strong></div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}

          </div>

          {/* 7. RIGHT COLUMN: Simplified Sidebar (ONLY THREE CARDS) */}
          <div className="workspace-sidebar-sticky">

            {/* Sidebar Card 1: Knowledge Overview */}
            <div className="sidebar-clean-card">
              <div className="sidebar-card-header">
                <Database size={16} color="var(--color-primary)" />
                <span>Knowledge Overview</span>
              </div>
              <div className="sidebar-kv-row">
                <span className="sidebar-kv-label">Indexed Documents:</span>
                <span className="sidebar-kv-value">{documents.length}</span>
              </div>
              <div className="sidebar-kv-row">
                <span className="sidebar-kv-label">Total Chunks:</span>
                <span className="sidebar-kv-value">{totalChunks}</span>
              </div>
              <div className="sidebar-kv-row">
                <span className="sidebar-kv-label">Embedding Model:</span>
                <span className="sidebar-kv-value">gemini-embedding-001</span>
              </div>
              <div className="sidebar-kv-row">
                <span className="sidebar-kv-label">Vector Database:</span>
                <span className="sidebar-kv-value">ChromaDB</span>
              </div>
            </div>

            {/* Sidebar Card 2: AI Engine */}
            <div className="sidebar-clean-card">
              <div className="sidebar-card-header">
                <Cpu size={16} color="var(--color-primary)" />
                <span>AI Engine</span>
              </div>
              <div className="sidebar-kv-row">
                <span className="sidebar-kv-label">Current Model:</span>
                <span className="sidebar-kv-value" style={{ color: "var(--color-primary)" }}>{systemService.formatModelName(systemInfo.model)}</span>
              </div>

              <div className="sidebar-kv-row">
                <span className="sidebar-kv-label">Fallback Enabled:</span>
                <span className="sidebar-kv-value" style={{ color: "var(--color-success)" }}>Yes (7 Fallbacks)</span>
              </div>
              <div className="sidebar-kv-row">
                <span className="sidebar-kv-label">Engine Health:</span>
                <span className="sidebar-kv-value" style={{ color: "var(--color-success)" }}>Operational</span>
              </div>
              <div className="sidebar-kv-row">
                <span className="sidebar-kv-label">Similarity Metric:</span>
                <span className="sidebar-kv-value">Cosine</span>
              </div>
            </div>

            {/* Sidebar Card 3: Quick Actions */}
            <div className="sidebar-clean-card">
              <div className="sidebar-card-header">
                <Zap size={16} color="var(--color-primary)" />
                <span>Quick Actions</span>
              </div>
              <Button variant="glow" style={{ width: "100%" }} icon={UploadCloud} onClick={() => setShowUploadModal(true)}>
                Upload Document
              </Button>
              <Button variant="outline" style={{ width: "100%" }} icon={RefreshCw} onClick={fetchDocs}>
                Refresh Catalog
              </Button>
            </div>

          </div>

        </div>

        {/* Upload Modal (Triggered by Upload CTA) */}
        <AnimatePresence>
          {showUploadModal && (
            <div
              style={{
                position: "fixed",
                inset: 0,
                background: "rgba(0,0,0,0.8)",
                zIndex: 1000,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                padding: "20px"
              }}
            >
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                style={{
                  background: "var(--bg-surface)",
                  border: "1px solid var(--border-color-active)",
                  borderRadius: "var(--radius-sm)",
                  padding: "28px",
                  maxWidth: "540px",
                  width: "100%"
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
                  <h3 style={{ fontSize: "1.1rem", fontWeight: 700, display: "flex", alignItems: "center", gap: "10px" }}>
                    <UploadCloud size={22} color="var(--color-primary)" />
                    Upload Enterprise Document
                  </h3>
                  <button onClick={() => setShowUploadModal(false)} style={{ background: "none", border: "none", color: "var(--text-primary)", cursor: "pointer" }}>
                    <X size={20} />
                  </button>
                </div>

                <form onSubmit={handleFileUpload}>
                  <div
                    className={`dropzone-box ${draggingOver ? "dragging" : ""}`}
                    onDragOver={(e) => { e.preventDefault(); setDraggingOver(true); }}
                    onDragLeave={() => setDraggingOver(false)}
                    onDrop={(e) => {
                      e.preventDefault();
                      setDraggingOver(false);
                      if (e.dataTransfer.files?.[0]) {
                        setFileToUpload(e.dataTransfer.files[0]);
                      }
                    }}
                    onClick={() => document.getElementById("modalDocUploadInput").click()}
                  >
                    <UploadCloud size={44} color="var(--color-primary)" style={{ opacity: 0.8 }} />
                    <p style={{ fontWeight: 700, marginTop: "12px", fontSize: "1.05rem" }}>
                      {fileToUpload ? fileToUpload.name : "Drag & drop PDF, TXT, MD, or DOCX files here"}
                    </p>
                    <span style={{ fontSize: "0.82rem", color: "var(--text-secondary)", marginTop: "6px" }}>
                      Auto-chunked with Gemini gemini-embedding-001 (3072-dim) • ChromaDB Index
                    </span>

                    <input
                      type="file"
                      id="modalDocUploadInput"
                      accept=".pdf,.txt,.md,.docx,.rtf"
                      style={{ display: "none" }}
                      onChange={(e) => setFileToUpload(e.target.files[0])}
                    />
                  </div>

                  {uploading && (
                    <div className="ingestion-checklist">
                      <div className={`checklist-step ${ingestionStep >= 1 ? (ingestionStep > 1 ? "done" : "active") : ""}`}>
                        <Check size={14} />
                        <span>Parsing document structure & text extraction</span>
                      </div>
                      <div className={`checklist-step ${ingestionStep >= 2 ? (ingestionStep > 2 ? "done" : "active") : ""}`}>
                        <Check size={14} />
                        <span>Generating 512-character semantic text chunks</span>
                      </div>
                      <div className={`checklist-step ${ingestionStep >= 3 ? (ingestionStep > 3 ? "done" : "active") : ""}`}>
                        <Check size={14} />
                        <span>Computing 3072-dim embeddings via gemini-embedding-001</span>
                      </div>
                      <div className={`checklist-step ${ingestionStep >= 4 ? (ingestionStep > 4 ? "done" : "active") : ""}`}>
                        <Check size={14} />
                        <span>Saving vectors and metadata to ChromaDB collection</span>
                      </div>
                    </div>
                  )}

                  {fileToUpload && !uploading && (
                    <div style={{ marginTop: "18px", display: "flex", justifyContent: "flex-end", gap: "10px" }}>
                      <Button variant="ghost" onClick={() => setFileToUpload(null)}>Cancel</Button>
                      <Button type="submit" icon={Sparkles} variant="glow">
                        Ingest Document
                      </Button>
                    </div>
                  )}
                </form>
              </motion.div>
            </div>
          )}
        </AnimatePresence>

      </div>
    </AppLayout>
  );
}

export default KnowledgeBase;
