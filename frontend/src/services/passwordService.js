import api from "./api";
import { supabase } from "./supabaseClient";

/**
 * Service for managing password reset and synchronization
 * between Supabase Auth email recovery and the FastAPI SQL database.
 */
export const passwordService = {
  /**
   * Sends a password reset email via Supabase Auth.
   * Never exposes whether an email exists in the system for security.
   */
  async sendResetEmail(email) {
    const rawAppUrl = import.meta.env.VITE_APP_URL || window.location.origin;
    const appUrl = rawAppUrl.replace(/\/+$/, "");
    const redirectTo = `${appUrl}/reset-password`;

    try {
      await supabase.auth.resetPasswordForEmail(email, {
        redirectTo,
      });
    } catch (err) {
      console.warn("Supabase reset email warning:", err);
    }

    // Always return generic success message to prevent user enumeration attacks
    return {
      success: true,
      message: "If an account exists for this email, a password reset link has been sent.",
    };
  },

  /**
   * Updates password in Supabase Auth recovery session,
   * then synchronizes the updated password hash with the FastAPI SQL database.
   */
  async updatePassword(newPassword, email) {
    // 1. Update password in Supabase Auth recovery session
    const { data: supabaseData, error: supabaseError } = await supabase.auth.updateUser({
      password: newPassword,
    });

    if (supabaseError) {
      throw new Error(supabaseError.message || "Failed to update password in identity provider.");
    }

    // Determine target email from parameter or active Supabase user session
    const targetEmail = email || supabaseData?.user?.email;

    if (!targetEmail) {
      throw new Error("Unable to determine user email for password update synchronization.");
    }

    // 2. Synchronize password update with FastAPI SQL database
    const response = await api.post("/auth/update-password", {
      email: targetEmail,
      new_password: newPassword,
    });

    return response.data;
  },

  /**
   * Gets current Supabase session to verify recovery token validity.
   */
  async getRecoverySession() {
    const { data, error } = await supabase.auth.getSession();
    if (error || !data?.session) {
      return null;
    }
    return data.session;
  },
};

export default passwordService;
