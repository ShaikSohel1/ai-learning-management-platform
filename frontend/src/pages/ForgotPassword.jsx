import React, { useState } from "react";
import { Link } from "react-router-dom";
import { BrainCircuit, Mail, ArrowLeft, Send } from "lucide-react";
import Card from "../components/common/Card";
import LoadingButton from "../components/common/LoadingButton";
import SuccessCard from "../components/common/SuccessCard";
import ToastNotification from "../components/common/ToastNotification";
import passwordService from "../services/passwordService";
import "../styles/login.css";

export function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [toast, setToast] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !email.includes("@")) {
      setToast({ type: "error", message: "Please enter a valid email address." });
      return;
    }

    setLoading(true);
    setToast(null);

    try {
      const res = await passwordService.sendResetEmail(email);
      setSubmitted(true);
      setToast({ type: "success", message: res.message });
    } catch (err) {
      console.error("Forgot password error:", err);
      // Security principle: Never reveal if email exists, show generic success
      setSubmitted(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-shell">
      <div className="login-card-wrapper">
        {submitted ? (
          <SuccessCard
            title="Check Your Email"
            description="If an account exists for this email address, a password reset link has been sent. Please check your inbox and follow the instructions."
            actionText="Return to Sign In"
            onAction={() => window.location.href = "/"}
          />
        ) : (
          <Card variant="glass" style={{ padding: "36px" }}>
            <div style={{ textAlign: "center", marginBottom: "24px" }}>
              <div className="login-brand-icon">
                <BrainCircuit size={28} />
              </div>
              <h1 style={{ fontSize: "1.6rem", fontWeight: 800, marginTop: "12px", letterSpacing: "-0.02em" }}>
                Reset Your Password
              </h1>
              <p style={{ fontSize: "0.88rem", color: "var(--text-muted)", marginTop: "4px" }}>
                Enter your work email address and we'll send you a password recovery link.
              </p>
            </div>

            <ToastNotification
              message={toast?.message}
              type={toast?.type}
              onClose={() => setToast(null)}
            />

            <form onSubmit={handleSubmit}>
              <div className="login-input-group">
                <label htmlFor="email">Email Address</label>
                <div className="login-input-box">
                  <Mail size={18} color="var(--text-muted)" />
                  <input
                    id="email"
                    type="email"
                    placeholder="jane@company.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
              </div>

              <LoadingButton
                type="submit"
                icon={Send}
                variant="glow"
                style={{ width: "100%", marginTop: "20px" }}
                loading={loading}
                loadingText="Sending Link..."
              >
                Send Reset Link
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
                  transition: "color 0.2s ease",
                }}
              >
                <ArrowLeft size={16} /> Back to Sign In
              </Link>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}

export default ForgotPassword;
