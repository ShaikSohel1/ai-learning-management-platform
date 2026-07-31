import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { BrainCircuit, KeyRound, AlertOctagon, ArrowLeft } from "lucide-react";
import Card from "../components/common/Card";
import PasswordInput from "../components/common/PasswordInput";
import PasswordStrengthMeter from "../components/common/PasswordStrengthMeter";
import LoadingButton from "../components/common/LoadingButton";
import SuccessCard from "../components/common/SuccessCard";
import ToastNotification from "../components/common/ToastNotification";
import passwordService from "../services/passwordService";
import { supabase } from "../services/supabaseClient";
import "../styles/login.css";

export function ResetPassword() {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [verifyingSession, setVerifyingSession] = useState(true);
  const [invalidLink, setInvalidLink] = useState(false);
  const [userEmail, setUserEmail] = useState("");
  const [success, setSuccess] = useState(false);
  const [toast, setToast] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    let mounted = true;

    async function checkRecoverySession() {
      try {
        // 1. Check existing session
        const session = await passwordService.getRecoverySession();
        if (session && session.user) {
          if (mounted) {
            setUserEmail(session.user.email);
            setVerifyingSession(false);
          }
          return;
        }

        // 2. Listen to Supabase auth state change (e.g., when magic link recovery token resolves)
        const { data: authListener } = supabase.auth.onAuthStateChange(async (event, session) => {
          if (event === "PASSWORD_RECOVERY" || (session && session.user)) {
            if (mounted) {
              setUserEmail(session?.user?.email || "");
              setInvalidLink(false);
              setVerifyingSession(false);
            }
          }
        });

        // Give auth listener a brief moment to process URL hash fragment
        setTimeout(() => {
          if (mounted && verifyingSession) {
            supabase.auth.getSession().then(({ data }) => {
              if (data?.session?.user) {
                setUserEmail(data.session.user.email);
                setInvalidLink(false);
              } else {
                setInvalidLink(true);
              }
              setVerifyingSession(false);
            });
          }
        }, 1200);

        return () => {
          authListener?.subscription?.unsubscribe();
        };
      } catch (err) {
        console.error("Recovery session error:", err);
        if (mounted) {
          setInvalidLink(true);
          setVerifyingSession(false);
        }
      }
    }

    checkRecoverySession();

    return () => {
      mounted = false;
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setToast(null);

    if (newPassword.length < 8) {
      setToast({ type: "error", message: "Password must be at least 8 characters long." });
      return;
    }

    if (newPassword !== confirmPassword) {
      setToast({ type: "error", message: "Passwords do not match." });
      return;
    }

    setLoading(true);

    try {
      await passwordService.updatePassword(newPassword, userEmail);
      setSuccess(true);
    } catch (err) {
      console.error("Password update error:", err);
      setToast({
        type: "error",
        message: err.response?.data?.detail || err.message || "Failed to update password.",
      });
    } finally {
      setLoading(false);
    }
  };

  if (verifyingSession) {
    return (
      <div className="login-shell">
        <div className="login-card-wrapper">
          <Card variant="glass" style={{ padding: "36px", textAlign: "center" }}>
            <div className="login-brand-icon" style={{ animation: "pulse 1.5s infinite" }}>
              <BrainCircuit size={28} />
            </div>
            <p style={{ marginTop: "16px", color: "var(--text-muted)", fontSize: "0.92rem" }}>
              Verifying security recovery link...
            </p>
          </Card>
        </div>
      </div>
    );
  }

  if (invalidLink) {
    return (
      <div className="login-shell">
        <div className="login-card-wrapper">
          <Card variant="glass" style={{ padding: "36px", textAlign: "center" }}>
            <div
              style={{
                width: "56px",
                height: "56px",
                borderRadius: "50%",
                background: "rgba(239, 68, 68, 0.15)",
                border: "1px solid rgba(239, 68, 68, 0.3)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                margin: "0 auto 20px auto",
              }}
            >
              <AlertOctagon size={32} color="#EF4444" />
            </div>
            <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "10px", color: "var(--text-primary)" }}>
              Invalid or Expired Link
            </h2>
            <p style={{ fontSize: "0.92rem", color: "var(--text-muted)", marginBottom: "24px", lineHeight: "1.5" }}>
              This password reset link is invalid, expired, or has already been used. Please request a new recovery link.
            </p>
            <Link to="/forgot-password" style={{ textDecoration: "none" }}>
              <LoadingButton variant="glow" style={{ width: "100%" }}>
                Request New Reset Link
              </LoadingButton>
            </Link>
          </Card>
        </div>
      </div>
    );
  }

  if (success) {
    return (
      <div className="login-shell">
        <div className="login-card-wrapper">
          <SuccessCard
            title="Password Updated!"
            description="Your password has been successfully updated across your account. You can now sign in with your new password."
            actionText="Sign In with New Password"
            onAction={() => navigate("/")}
          />
        </div>
      </div>
    );
  }

  return (
    <div className="login-shell">
      <div className="login-card-wrapper">
        <Card variant="glass" style={{ padding: "36px" }}>
          <div style={{ textAlign: "center", marginBottom: "24px" }}>
            <div className="login-brand-icon">
              <KeyRound size={28} />
            </div>
            <h1 style={{ fontSize: "1.6rem", fontWeight: 800, marginTop: "12px", letterSpacing: "-0.02em" }}>
              Create New Password
            </h1>
            <p style={{ fontSize: "0.88rem", color: "var(--text-muted)", marginTop: "4px" }}>
              Set a strong password for <strong style={{ color: "var(--text-primary)" }}>{userEmail || "your account"}</strong>
            </p>
          </div>

          <ToastNotification
            message={toast?.message}
            type={toast?.type}
            onClose={() => setToast(null)}
          />

          <form onSubmit={handleSubmit}>
            <PasswordInput
              id="newPassword"
              name="newPassword"
              label="New Password"
              placeholder="At least 8 characters"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />

            <PasswordStrengthMeter password={newPassword} />

            <PasswordInput
              id="confirmPassword"
              name="confirmPassword"
              label="Confirm New Password"
              placeholder="Re-enter new password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />

            <LoadingButton
              type="submit"
              variant="glow"
              style={{ width: "100%", marginTop: "20px" }}
              loading={loading}
              loadingText="Updating Password..."
            >
              Update Password
            </LoadingButton>
          </form>

          <div style={{ marginTop: "24px", textAlign: "center" }}>
            <Link
              to="/"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "6px",
                fontSize: "0.88rem",
                color: "var(--text-muted)",
                textDecoration: "none",
                fontWeight: 500,
              }}
            >
              <ArrowLeft size={16} /> Back to Sign In
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
}

export default ResetPassword;
