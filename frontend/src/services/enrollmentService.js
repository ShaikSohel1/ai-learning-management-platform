import api from "./api";

/**
 * Enrollment Service handling REST API calls to backend enrollment endpoints.
 */
export const enrollmentService = {
  /**
   * Fetches user's current course enrollments.
   * @returns {Promise<Array>} List of Enrollment objects
   */
  async getMyEnrollments() {
    const response = await api.get("/enrollments");
    return response.data;
  },

  /**
   * Gets specific enrollment details.
   * @param {number} enrollmentId
   * @returns {Promise<Object>} Enrollment details
   */
  async getEnrollment(enrollmentId) {
    const response = await api.get(`/enrollments/${enrollmentId}`);
    return response.data;
  },

  /**
   * Enrolls authenticated user into a course.
   * @param {number} courseId
   * @returns {Promise<Object>} Enrollment response
   */
  async enrollInCourse(courseId) {
    const response = await api.post("/enrollments", { course_id: courseId });
    return response.data;
  },

  /**
   * Updates course progress percentage.
   * @param {number} enrollmentId
   * @param {number} progressPercentage - 0 to 100
   * @returns {Promise<Object>} Updated enrollment
   */
  async updateProgress(enrollmentId, progressPercentage) {
    const response = await api.put(`/enrollments/${enrollmentId}/progress`, {
      progress_percentage: progressPercentage,
    });
    return response.data;
  },

  /**
   * Marks course as 100% completed and issues certificate.
   * @param {number} enrollmentId
   * @returns {Promise<Object>} Updated enrollment
   */
  async completeCourse(enrollmentId) {
    const response = await api.put(`/enrollments/${enrollmentId}/complete`);
    return response.data;
  },

  /**
   * Gets issued certificate details for a completed enrollment.
   * @param {number} enrollmentId
   * @returns {Promise<Object>} Certificate details
   */
  async getCertificate(enrollmentId) {
    const response = await api.get(`/enrollments/${enrollmentId}/certificate`);
    return response.data;
  },

  /**
   * Removes a course enrollment.
   * @param {number} enrollmentId
   * @returns {Promise<Object>} Confirmation message
   */
  async deleteEnrollment(enrollmentId) {
    const response = await api.delete(`/enrollments/${enrollmentId}`);
    return response.data;
  },
};

export default enrollmentService;
