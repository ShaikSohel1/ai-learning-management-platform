import api from "./api";

/**
 * Enterprise Service for managing token-based password reset flows
 * via FastAPI REST backend endpoints.
 */
export const passwordService = {
  /**
   * Sends a password reset request email via FastAPI backend.
   */
  async sendResetEmail(email) {
    const response = await api.post("/auth/forgot-password", { email });
    return response.data;
  },

  /**
   * Validates if a plaintext reset token is valid, unused, and unexpired.
   */
  async validateResetToken(token) {
    const response = await api.get(`/auth/validate-reset-token?token=${encodeURIComponent(token)}`);
    return response.data;
  },

  /**
   * Submits new password and confirmation to reset password via token.
   */
  async resetPassword(token, password, confirmPassword) {
    const response = await api.post("/auth/reset-password", {
      token,
      password,
      confirm_password: confirmPassword,
    });
    return response.data;
  },
};

export const authService = passwordService;

export default passwordService;
