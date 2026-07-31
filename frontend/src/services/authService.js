import api from "./api";

/**
 * Complete Authentication & Password Recovery Service.
 */
export const loginUser = async (email, password) => {
  const response = await api.post("/auth/login", { email, password });
  return response.data;
};

export const registerUser = async (userData) => {
  const response = await api.post("/auth/register", userData);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get("/auth/me");
  return response.data;
};

export const sendResetEmail = async (email) => {
  const response = await api.post("/auth/forgot-password", { email });
  return response.data;
};

export const validateResetToken = async (token) => {
  const response = await api.get(`/auth/validate-reset-token?token=${encodeURIComponent(token)}`);
  return response.data;
};

export const resetPassword = async (token, password, confirmPassword) => {
  const response = await api.post("/auth/reset-password", {
    token,
    password,
    confirm_password: confirmPassword,
  });
  return response.data;
};

export const authService = {
  loginUser,
  registerUser,
  getCurrentUser,
  sendResetEmail,
  validateResetToken,
  resetPassword,
};

export default authService;