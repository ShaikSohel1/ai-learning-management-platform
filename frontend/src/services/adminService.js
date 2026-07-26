import api from "./api";

/**
 * Admin Service handling REST API calls to backend Admin & Health endpoints.
 */
export const adminService = {
  /**
   * Fetches global enterprise statistics.
   * @returns {Promise<Object>} Admin stats summary
   */
  async getAdminStats() {
    const response = await api.get("/admin/stats");
    return response.data;
  },

  /**
   * Fetches registered users catalog.
   * @returns {Promise<Array>} List of users
   */
  async getAllUsers() {
    const response = await api.get("/admin/users");
    return response.data;
  },

  /**
   * Fetches component health status.
   * @returns {Promise<Object>} System health summary
   */
  async getSystemHealth() {
    const response = await api.get("/admin/system-health");
    return response.data;
  },
};

export default adminService;
