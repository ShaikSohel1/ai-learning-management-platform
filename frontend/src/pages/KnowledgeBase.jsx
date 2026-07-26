import { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import knowledgeService from "../services/knowledgeService";
import "../styles/knowledgeBase.css";

function KnowledgeBase() {
  const [activeTab, setActiveTab] = useState("chat"); // 'chat' | 'search' | 'library' | 'analytics'

  // Library State
  const [documents, setDocuments] = useState([]);
  const [loadingDocs, setLoadingDocs] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState("");
  const [uploadError, setUploadError] = useState("");

  // Ask Chat State
  const [question, setQuestion] = useState("");
  const [loadingAsk, setLoadingAsk] = useState(false);
  const [askError, setAskError] = useState("");
  const [ragResult, setRagResult] = useState(null);

  // Semantic Search State
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedDocFilter, setSelectedDocFilter] = useState("");
  const [loadingSearch, setLoadingSearch] = useState(false);
  const [searchResults, setSearchResults] = useState(null);

  // Analytics & History State
  const [stats, setStats] = useState(null);
  const [searchHistory, setSearchHistory] = useState([]);
  const [loadingStats, setLoadingStats] = useState(false);

  const loadDocuments = async () => {
    try {
      setLoadingDocs(true);
      const docs = await knowledgeService.getDocuments();
      setDocuments(docs);
    } catch (err) {
      console.error("Failed to load documents:", err);
    } finally {
      setLoadingDocs(false);
    }
  };

  const loadAnalyticsAndHistory = async () => {
    try {
      setLoadingStats(true);
      const [statsData, historyData] = await Promise.all([
        knowledgeService.getStatistics(),
        knowledgeService.getSearchHistory(),
      ]);
      setStats(statsData);
      setSearchHistory(historyData);
    } catch (err) {
      console.error("Failed to load analytics & history:", err);
    } finally {
      setLoadingStats(false);
    }
  };

  useEffect(() => {
    loadDocuments();
    loadAnalyticsAndHistory();
  }, []);

  // Handler: File Upload
  const handleFileUpload = async (file) => {
    if (!file) return;

    setUploading(true);
    setUploadError("");
    setUploadSuccess("");

    try {
      const res = await knowledgeService.uploadDocument(file);
      setUploadSuccess(
        `Successfully ingested "${res.document_name}" into vector store (${res.chunk_count} chunks, ${res.document_size}).`
      );
      loadDocuments();
      loadAnalyticsAndHistory();
    } catch (err) {
      console.error("Document upload error:", err);
      setUploadError(
        err.response?.data?.detail || "Failed to upload and ingest document."
      );
    } finally {
      setUploading(false);
    }
  };

  const handleFileInputChange = (e) => {
    const file = e.target.files[0];
    if (file) handleFileUpload(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  // Handler: Delete Document
  const handleDeleteDocument = async (docId, docName) => {
    if (!window.confirm(`Delete document "${docName}" from vector store?`)) return;

    try {
      await knowledgeService.deleteDocument(docId);
      loadDocuments();
      loadAnalyticsAndHistory();
    } catch (err) {
      console.error("Failed to delete document:", err);
      alert(err.response?.data?.detail || "Could not delete document.");
    }
  };

  // Handler: Ask RAG Question
  const handleAskQuestion = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoadingAsk(true);
    setAskError("");
    setRagResult(null);

    try {
      const res = await knowledgeService.askKnowledge({
        question: question.trim(),
        top_k: 4,
        threshold: 0.3,
      });
      setRagResult(res);
      loadAnalyticsAndHistory();
    } catch (err) {
      console.error("RAG ask error:", err);
      setAskError(
        err.response?.data?.detail || "Failed to answer question via Knowledge Base."
      );
    } finally {
      setLoadingAsk(false);
    }
  };

  // Handler: Semantic Search
  const handleSemanticSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoadingSearch(true);
    try {
      const res = await knowledgeService.semanticSearch({
        query: searchQuery.trim(),
        top_k: 6,
        threshold: 0.25,
        filename_filter: selectedDocFilter || undefined,
      });
      setSearchResults(res);
    } catch (err) {
      console.error("Semantic search error:", err);
    } finally {
      setLoadingSearch(false);
    }
  };

  // Handler: Clear History Log
  const handleClearHistory = async () => {
    try {
      await knowledgeService.clearSearchHistory();
      setSearchHistory([]);
      loadAnalyticsAndHistory();
    } catch (err) {
      console.error("Failed to clear search history:", err);
    }
  };

  return (
    <div>
      <Navbar />

      <div className="knowledge-container">
        {/* Header Banner */}
        <div className="knowledge-header">
          <h1>⚡ Enterprise Semantic Search Platform</h1>
          <p>
            Upgrade your retrieval capabilities with hybrid vector search, query understanding, reranking, and confidence scoring.
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="knowledge-tabs">
          <button
            className={`knowledge-tab-btn ${activeTab === "chat" ? "active" : ""}`}
            onClick={() => setActiveTab("chat")}
          >
            💬 Knowledge Chat (RAG)
          </button>
          <button
            className={`knowledge-tab-btn ${activeTab === "search" ? "active" : ""}`}
            onClick={() => setActiveTab("search")}
          >
            🔎 Semantic Search Engine
          </button>
          <button
            className={`knowledge-tab-btn ${activeTab === "library" ? "active" : ""}`}
            onClick={() => setActiveTab("library")}
          >
            📚 Vector Document Catalog ({documents.length})
          </button>
          <button
            className={`knowledge-tab-btn ${activeTab === "analytics" ? "active" : ""}`}
            onClick={() => {
              setActiveTab("analytics");
              loadAnalyticsAndHistory();
            }}
          >
            📈 Analytics & History
          </button>
        </div>

        {/* Tab 1: Knowledge Chat (RAG) */}
        {activeTab === "chat" && (
          <div>
            <div className="knowledge-card">
              <h2 className="knowledge-card-title">🔍 Enterprise Knowledge QA</h2>

              {askError && <div className="error-banner">{askError}</div>}

              <form onSubmit={handleAskQuestion}>
                <div className="form-group">
                  <label htmlFor="ragQuestion">Enterprise Policy, Technical & SOP Query</label>
                  <div style={{ display: "flex", gap: "10px" }}>
                    <input
                      id="ragQuestion"
                      type="text"
                      className="form-control"
                      placeholder="e.g. What is our employee annual leave policy or deployment procedure?"
                      value={question}
                      onChange={(e) => setQuestion(e.target.value)}
                      required
                    />
                    <button
                      type="submit"
                      className="btn-ai-primary"
                      style={{ width: "auto", padding: "0 28px", whiteSpace: "nowrap" }}
                      disabled={loadingAsk}
                    >
                      {loadingAsk ? "Retrieving..." : "Ask RAG"}
                    </button>
                  </div>
                </div>
              </form>
            </div>

            {/* Loading Indicator */}
            {loadingAsk && (
              <div className="knowledge-card">
                <div className="loading-pulse">
                  <div className="pulse-dot"></div>
                  <div className="pulse-dot"></div>
                  <div className="pulse-dot"></div>
                  <span>Running Hybrid Vector + Keyword Search, Reranking & Sentence Compression...</span>
                </div>
              </div>
            )}

            {/* RAG Answer Display */}
            {ragResult && !loadingAsk && (
              <div className="knowledge-card">
                <div className="rag-answer-box">
                  <div className="rag-header-meta">
                    {ragResult.rag_used ? (
                      <span className="rag-header-badge badge-rag-active">
                        📖 Hybrid Verified Document Context
                      </span>
                    ) : (
                      <span className="rag-header-badge badge-rag-fallback">
                        🤖 Gemini Model Fallback
                      </span>
                    )}

                    <span className="rag-header-badge badge-confidence">
                      🎯 Confidence: {ragResult.confidence_score}%
                    </span>

                    <span className="rag-header-badge badge-latency">
                      ⚡ Latency: {ragResult.response_time_ms} ms
                    </span>

                    <span className="rag-header-badge badge-intent">
                      🏷️ Intent: {ragResult.search_intent}
                    </span>
                  </div>

                  <div className="rag-answer-text">{ragResult.answer}</div>

                  {/* Referenced Documents */}
                  {ragResult.referenced_documents?.length > 0 && (
                    <div style={{ marginTop: "15px", fontSize: "0.88rem", color: "#047857" }}>
                      <strong>Referenced Documents:</strong> {ragResult.referenced_documents.join(", ")}
                    </div>
                  )}
                </div>

                {/* Reranked Source Citations */}
                {ragResult.citations?.length > 0 && (
                  <div>
                    <h4 className="citations-title">
                      📎 Reranked Vector Source Citations ({ragResult.citations.length})
                    </h4>

                    <div className="citations-grid">
                      {ragResult.citations.map((cite, idx) => (
                        <div key={idx} className="citation-card">
                          <div className="citation-head">
                            <span className="citation-doc">
                              📄 {cite.document_name} (Chunk {cite.chunk_index})
                            </span>
                            <span className="citation-score">
                              {Math.round(cite.similarity_score * 100)}% Match
                            </span>
                          </div>
                          <div className="citation-snippet">"{cite.snippet}"</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Tab 2: Hybrid Semantic Search Engine */}
        {activeTab === "search" && (
          <div>
            <div className="knowledge-card">
              <h2 className="knowledge-card-title">🔎 Hybrid Semantic & Keyword Search</h2>

              <form onSubmit={handleSemanticSearch}>
                <div className="form-group">
                  <label htmlFor="searchQuery">Search Query</label>
                  <div style={{ display: "flex", gap: "10px" }}>
                    <input
                      id="searchQuery"
                      type="text"
                      className="form-control"
                      placeholder="Search enterprise documents..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      required
                    />

                    <select
                      className="form-control"
                      style={{ width: "200px" }}
                      value={selectedDocFilter}
                      onChange={(e) => setSelectedDocFilter(e.target.value)}
                    >
                      <option value="">All Documents</option>
                      {documents.map((d) => (
                        <option key={d.document_id} value={d.document_name}>
                          {d.document_name}
                        </option>
                      ))}
                    </select>

                    <button
                      type="submit"
                      className="btn-ai-primary"
                      style={{ width: "auto", padding: "0 28px", whiteSpace: "nowrap" }}
                      disabled={loadingSearch}
                    >
                      Search
                    </button>
                  </div>
                </div>
              </form>
            </div>

            {/* Search Results Display */}
            {searchResults && (
              <div className="knowledge-card">
                <div className="rag-header-meta" style={{ marginBottom: "20px" }}>
                  <span className="rag-header-badge badge-confidence">
                    Overall Score: {searchResults.confidence_score}%
                  </span>
                  <span className="rag-header-badge badge-intent">
                    Intent: {searchResults.search_intent}
                  </span>
                  <span>Results Count: {searchResults.results_count}</span>
                </div>

                {searchResults.citations?.length === 0 ? (
                  <p style={{ color: "#64748b" }}>No vector chunks matched your search criteria.</p>
                ) : (
                  <div className="citations-grid">
                    {searchResults.citations.map((cite, idx) => (
                      <div key={idx} className="citation-card">
                        <div className="citation-head">
                          <span className="citation-doc">
                            📄 {cite.document_name} (Chunk {cite.chunk_index})
                          </span>
                          <span className="citation-score">
                            {Math.round(cite.similarity_score * 100)}% Confidence
                          </span>
                        </div>
                        <div className="citation-snippet">"{cite.snippet}"</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Tab 3: Document Library & Upload */}
        {activeTab === "library" && (
          <div>
            <div className="knowledge-card">
              <h2 className="knowledge-card-title">📤 Upload Enterprise Document</h2>

              {uploadSuccess && <div className="success-banner">{uploadSuccess}</div>}
              {uploadError && <div className="error-banner">{uploadError}</div>}

              <div
                className="dropzone"
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => document.getElementById("fileInput").click()}
              >
                <div className="dropzone-icon">📁</div>
                <p>
                  {uploading
                    ? "Processing document, generating overlapping chunks & vector embeddings..."
                    : "Drag & drop document here, or click to browse"}
                </p>
                <span>Supported Formats: .pdf, .txt, .md, .docx</span>
                <input
                  id="fileInput"
                  type="file"
                  accept=".pdf,.txt,.md,.markdown,.docx"
                  style={{ display: "none" }}
                  onChange={handleFileInputChange}
                  disabled={uploading}
                />
              </div>
            </div>

            <div className="knowledge-card">
              <h2 className="knowledge-card-title">
                📚 Vector Document Catalog ({documents.length})
              </h2>

              {loadingDocs ? (
                <p style={{ textAlign: "center", color: "#64748b" }}>
                  Loading document catalog from ChromaDB...
                </p>
              ) : documents.length === 0 ? (
                <div style={{ textAlign: "center", padding: "30px 0", color: "#64748b" }}>
                  No documents in vector store yet. Upload your first document above.
                </div>
              ) : (
                <table className="docs-table">
                  <thead>
                    <tr>
                      <th>Document Name</th>
                      <th>Uploaded By</th>
                      <th>Upload Date</th>
                      <th>Chunks / Vectors</th>
                      <th>Size</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {documents.map((doc) => (
                      <tr key={doc.document_id}>
                        <td>
                          <div className="doc-name">📄 {doc.document_name}</div>
                        </td>
                        <td>{doc.uploaded_by}</td>
                        <td>
                          {doc.upload_date
                            ? new Date(doc.upload_date).toLocaleDateString()
                            : "N/A"}
                        </td>
                        <td>
                          <span style={{ fontWeight: 700, color: "#059669" }}>
                            {doc.chunk_count} Chunks
                          </span>
                        </td>
                        <td>{doc.document_size}</td>
                        <td>
                          <button
                            className="btn-delete-doc"
                            onClick={() =>
                              handleDeleteDocument(
                                doc.document_id,
                                doc.document_name
                              )
                            }
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}

        {/* Tab 4: Analytics & History */}
        {activeTab === "analytics" && (
          <div>
            {/* Analytics Stats Widgets */}
            <div className="analytics-grid">
              <div className="analytics-card">
                <div className="analytics-icon">📄</div>
                <div>
                  <div className="analytics-val">{stats?.total_documents || 0}</div>
                  <div className="analytics-lbl">Total Documents</div>
                </div>
              </div>

              <div className="analytics-card">
                <div className="analytics-icon">🧩</div>
                <div>
                  <div className="analytics-val">{stats?.total_chunks || 0}</div>
                  <div className="analytics-lbl">Total Text Chunks</div>
                </div>
              </div>

              <div className="analytics-card">
                <div className="analytics-icon">⚡</div>
                <div>
                  <div className="analytics-val">{stats?.avg_response_time_ms || 0} ms</div>
                  <div className="analytics-lbl">Avg Search Latency</div>
                </div>
              </div>

              <div className="analytics-card">
                <div className="analytics-icon">🎯</div>
                <div>
                  <div className="analytics-val">{stats?.avg_confidence_score || 0}%</div>
                  <div className="analytics-lbl">Avg Confidence</div>
                </div>
              </div>
            </div>

            {/* Search History Log Table */}
            <div className="knowledge-card">
              <div className="knowledge-card-title">
                <span>🕒 Recent Search History ({searchHistory.length})</span>
                <button
                  onClick={handleClearHistory}
                  className="btn-delete-doc"
                  style={{ fontSize: "0.8rem" }}
                >
                  Clear History Log
                </button>
              </div>

              {searchHistory.length === 0 ? (
                <p style={{ color: "#64748b", padding: "10px 0" }}>
                  No previous search queries logged yet.
                </p>
              ) : (
                <table className="history-table">
                  <thead>
                    <tr>
                      <th>Query Question</th>
                      <th>Timestamp</th>
                      <th>Latency</th>
                      <th>Confidence</th>
                      <th>Sources Used</th>
                    </tr>
                  </thead>
                  <tbody>
                    {searchHistory.map((item) => (
                      <tr key={item.entry_id}>
                        <td style={{ fontWeight: 600 }}>{item.question}</td>
                        <td>{new Date(item.timestamp).toLocaleTimeString()}</td>
                        <td>{item.response_time_ms} ms</td>
                        <td>
                          <span style={{ fontWeight: 700, color: "#0369a1" }}>
                            {item.confidence_score}%
                          </span>
                        </td>
                        <td>
                          {item.documents_used?.length > 0
                            ? item.documents_used.join(", ")
                            : "Gemini Fallback"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default KnowledgeBase;
