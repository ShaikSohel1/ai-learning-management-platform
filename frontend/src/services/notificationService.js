import api from "./api";

/**
 * Notification Service handling REST API calls to backend Notification Center endpoints.
 */
export const notificationService = {
  /**
   * Fetches list of user notifications.
   * @returns {Promise<Array>} List of NotificationResponse objects
   */
  async getNotifications() {
    const response = await api.get("/notifications");
    return response.data;
  },

  /**
   * Creates a notification.
   * @param {Object} data - { title: string, message: string, notification_type?: string }
   * @returns {Promise<Object>} NotificationResponse
   */
  async createNotification(data) {
    const response = await api.post("/notifications", data);
    return response.data;
  },

  /**
   * Marks a notification as read.
   * @param {number} notificationId
   * @returns {Promise<Object>} Status response
   */
  async markAsRead(notificationId) {
    const response = await api.put(`/notifications/${notificationId}/read`);
    return response.data;
  },

  /**
   * Deletes a notification.
   * @param {number} notificationId
   * @returns {Promise<Object>} Status response
   */
  async deleteNotification(notificationId) {
    const response = await api.delete(`/notifications/${notificationId}`);
    return response.data;
  },
};

export default notificationService;
