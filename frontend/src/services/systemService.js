import api from "./api";

/**
 * System & AI Info Service to dynamically fetch active model & platform status.
 */
export const systemService = {
  /**
   * Fetches active AI provider, model, and system status from backend.
   * @returns {Promise<{ provider: string, model: string, status: string }>}
   */
  async getSystemInfo() {
    try {
      const response = await api.get("/system/info");
      return response.data;
    } catch (error) {
      console.warn("Failed to fetch /system/info, falling back to /health/ai", error);
      try {
        const fallback = await api.get("/health/ai");
        return {
          provider: fallback.data?.provider || "Google Gemini",
          model: fallback.data?.model || "models/gemini-2.5-flash",
          status: fallback.data?.status || "Operational",
        };
      } catch (err) {
        return {
          provider: "Google Gemini",
          model: "models/gemini-2.5-flash",
          status: "Operational",
        };
      }
    }
  },

  /**
   * Formats raw model string (e.g., 'models/gemini-2.5-flash' -> 'Gemini 2.5 Flash').
   * @param {string} rawModel
   * @returns {string}
   */
  formatModelName(rawModel) {
    if (!rawModel) return "Gemini 2.5 Flash";
    let name = rawModel.replace("models/", "");
    const parts = name.split("-");
    return parts
      .map((p) => (p.match(/^\d+(\.\d+)?$/) ? p : p.charAt(0).toUpperCase() + p.slice(1)))
      .join(" ");
  },
};

export default systemService;
