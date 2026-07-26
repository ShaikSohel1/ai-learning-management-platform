import api from "./api";

/**
 * Agent Service handling REST API calls to backend Agentic AI Platform endpoints.
 */
export const agentService = {
  /**
   * Sends user message or goal to Agentic AI platform.
   * @param {Object} data - { message: string, career_goal?: string, current_skills?: Array }
   * @returns {Promise<Object>} AgentChatResponse
   */
  async sendAgentChat(data) {
    const response = await api.post("/agents/chat", data);
    return response.data;
  },

  /**
   * Triggers specific workflow pipeline execution.
   * @param {Object} data - { pipeline_type: string, career_goal: string, current_skills?: Array }
   * @returns {Promise<Object>} AgentChatResponse
   */
  async executeWorkflow(data) {
    const response = await api.post("/agents/workflow", data);
    return response.data;
  },

  /**
   * Fetches status of all platform agents.
   * @returns {Promise<Object>} AgentSystemStatusResponse
   */
  async getAgentsStatus() {
    const response = await api.get("/agents/status");
    return response.data;
  },

  /**
   * Lists available executable tools in Tool Registry.
   * @returns {Promise<Object>} Tools list
   */
  async getTools() {
    const response = await api.get("/agents/tools");
    return response.data;
  },

  /**
   * Executes a direct tool call.
   * @param {string} toolName
   * @param {Object} args
   * @returns {Promise<Object>} ToolCallRecord
   */
  async executeTool(toolName, args = {}) {
    const response = await api.post("/agents/execute", {
      tool_name: toolName,
      arguments: args,
    });
    return response.data;
  },

  /**
   * Gets user agent decision memory logs.
   * @returns {Promise<Object>} Memory summary
   */
  async getAgentHistory() {
    const response = await api.get("/agents/history");
    return response.data;
  },
};

export default agentService;
