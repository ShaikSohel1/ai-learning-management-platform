import api from "./api";

/**
 * AI Assistant Service handling calls to FastAPI backend AI endpoints.
 */
export const aiService = {
  /**
   * Generates a personalized learning path and course recommendations.
   * @param {Object} data - { career_goal: string, current_skills: string[] }
   * @returns {Promise<Object>} LearningPathResponse
   */
  async generateLearningPath(data) {
    const response = await api.post("/ai/learning-path", data);
    return response.data;
  },

  /**
   * Sends a chat message to multi-turn AI assistant.
   * @param {Object} data - { message: string, career_goal?: string, current_skills?: string[] }
   * @returns {Promise<Object>} AIChatResponse
   */
  async sendMessage(data) {
    const response = await api.post("/ai/chat", data);
    return response.data;
  },

  /**
   * Clears the user's multi-turn conversation memory history.
   * @returns {Promise<Object>} Status response
   */
  async clearHistory() {
    const response = await api.delete("/ai/history");
    return response.data;
  },
};

export default aiService;
