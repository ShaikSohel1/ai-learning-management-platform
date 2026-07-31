import React, { useState, useEffect } from "react";
import { useNavigate, useSearchParams, Link } from "react-router-dom";
import { BrainCircuit, KeyRound, AlertOctagon, ArrowLeft } from "lucide-react";
import Card from "../components/common/Card";
import PasswordInput from "../components/common/PasswordInput";
import PasswordStrengthMeter from "../components/common/PasswordStrengthMeter";
import LoadingButton from "../components/common/LoadingButton";
import SuccessCard from "../components/common/SuccessCard";
import ToastNotification from "../components/common/ToastNotification";
import passwordService from "../services/passwordService";
import "../styles/login.css";

export function ResetPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [verifyingSession, setVerifyingSession] = useState(true);
  const [invalidLink, setInvalidLink] = useState(false);
  const [invalidReason, setInvalidReason] = useState("");
  const [userEmail, setUserEmail] = useState("");
  const [success, setSuccess] = useState(false);
  const [toast, setToast] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    let mounted = true;

    async function checkTokenValidity() {
      if (!token) {
        if (mounted) {
          setInvalidLink(true);
          setInvalidReason("No recovery token was provided in the URL.");
          setVerifyingSession(false);
        }
        return;
      }

      try {
        const res = await passwordService.validateResetToken(token);
        if (mounted) {
          if (res.valid) {
            setUserEmail(res.email || "");
            setInvalidLink(false);
          } else {
            setInvalidLink(true);
            if (res.reason === "expired") {
              setInvalidReason("This password reset link has expired (30-minute limit).");
            } else if (res.reason === "used") {
              setInvalidReason("This password reset link has already been used.");
            } else {
              setInvalidReason("This password reset link is invalid or malformed.");
            }
          }
          setVerifyingSession(false);
        }
      } catch (err) {
        console.error("Token validation error:", err);
        if (mounted) {
          setInvalidLink(true);
          setInvalidReason("Unable to validate security token.");
          setVerifyingSession(false);
        }
      }
    }

    checkTokenValidity();

    return () => {
      mounted = false;
    };
  }, [token]);

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
      await passwordService.resetPassword(token, newPassword, confirmPassword);
      setSuccess(true);
    } catch (err) {
      console.error("Password update error:", err);
      setToast({
        type: "error",
        message: err.response?.data?.detail || err.message || "Failed to reset password.",
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
              Verifying security reset token...
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
              {invalidReason || "This password reset link is invalid or has expired. Please request a new recovery link."}
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
