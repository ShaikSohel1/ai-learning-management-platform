import api from "./api";

/**
 * System & AI Info Service to dynamically fetch active AI provider, model, and status.
 */
export const systemService = {
  /**
   * Fetches active AI provider, model, health, and fallback models from backend.
   * Primary endpoint: GET /ai/provider-status
   * @returns {Promise<{ provider: string, model: string, healthy: boolean, fallback_models: string[], status: string }>}
   */
  async getSystemInfo() {
    try {
      const response = await api.get("/ai/provider-status");
      return {
        provider: response.data?.provider || "Gemini",
        model: response.data?.model || "models/gemini-2.0-flash",
        healthy: response.data?.healthy ?? true,
        fallback_models: response.data?.fallback_models || [],
        status: response.data?.healthy !== false ? "Operational" : "Degraded",
      };
    } catch (error) {
      console.warn("Failed to fetch /ai/provider-status, falling back to /system/info", error);
      try {
        const fallback = await api.get("/system/info");
        return {
          provider: fallback.data?.provider || "Gemini",
          model: fallback.data?.model || "models/gemini-2.0-flash",
          healthy: true,
          fallback_models: [],
          status: fallback.data?.status || "Operational",
        };
      } catch (err) {
        return {
          provider: "Gemini",
          model: "models/gemini-2.0-flash",
          healthy: true,
          fallback_models: [],
          status: "Operational",
        };
      }
    }
  },

  /**
   * Formats raw model string dynamically (e.g. 'llama-3.3-70b-versatile' -> 'Llama 3.3 70B Versatile', 'openai/gpt-oss-20b' -> 'GPT-OSS 20B').
   * @param {string} rawModel
   * @returns {string}
   */
  formatModelName(rawModel) {
    if (!rawModel) return "AI Model";
    let name = rawModel.replace("models/", "").replace("openai/", "").replace("meta-llama/", "");
    const parts = name.split("-");
    return parts
      .map((p) => (p.match(/^\d+(\.\d+)?$/) ? p : p.charAt(0).toUpperCase() + p.slice(1)))
      .join(" ");
  },
};

export default systemService;
