import api from "./api";

/**
 * Knowledge Base Service handling REST API calls to backend RAG & Semantic Search endpoints.
 */
export const knowledgeService = {
  /**
   * Uploads an enterprise document (PDF, TXT, MD, DOCX).
   * @param {File} file
   * @returns {Promise<Object>} DocumentMetadata
   */
  async uploadDocument(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post("/knowledge/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },

  /**
   * Fetches list of uploaded knowledge base documents.
   * @returns {Promise<Array>} List of DocumentMetadata objects
   */
  async getDocuments() {
    const response = await api.get("/knowledge/documents");
    return response.data;
  },

  /**
   * Performs vector similarity search.
   * @param {string} query
   * @param {number} topK
   * @returns {Promise<Object>} Search results
   */
  async searchKnowledge(query, topK = 4) {
    const response = await api.get("/knowledge/search", {
      params: { query, top_k: topK },
    });
    return response.data;
  },

  /**
   * Advanced hybrid semantic search.
   * @param {Object} data - { query: string, top_k?: number, threshold?: number, filename_filter?: string }
   * @returns {Promise<Object>} Search results with reranked citations and intent
   */
  async semanticSearch(data) {
    const response = await api.post("/knowledge/semantic-search", data);
    return response.data;
  },

  /**
   * Asks RAG Knowledge Chat question.
   * @param {Object} data - { question: string, top_k?: number, threshold?: number }
   * @returns {Promise<Object>} KnowledgeAskResponse
   */
  async askKnowledge(data) {
    const response = await api.post("/knowledge/ask", data);
    return response.data;
  },

  /**
   * Gets user search history logs.
   * @returns {Promise<Array>} List of SearchHistoryItem objects
   */
  async getSearchHistory() {
    const response = await api.get("/knowledge/history");
    return response.data;
  },

  /**
   * Clears user search history logs.
   * @returns {Promise<Object>} Confirmation response
   */
  async clearSearchHistory() {
    const response = await api.delete("/knowledge/history");
    return response.data;
  },

  /**
   * Gets Knowledge Base analytics metrics summary.
   * @returns {Promise<Object>} KnowledgeAnalyticsResponse
   */
  async getStatistics() {
    const response = await api.get("/knowledge/statistics");
    return response.data;
  },

  /**
   * Triggers ChromaDB collection re-indexing.
   * @returns {Promise<Object>} Re-index response
   */
  async reindexCollection() {
    const response = await api.post("/knowledge/reindex");
    return response.data;
  },

  /**
   * Deletes document from vector store.
   * @param {string} documentId
   * @returns {Promise<Object>} Status response
   */
  async deleteDocument(documentId) {
    const response = await api.delete(`/knowledge/${documentId}`);
    return response.data;
  },
};

export default knowledgeService;
