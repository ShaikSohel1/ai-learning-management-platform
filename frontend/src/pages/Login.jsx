import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { BrainCircuit, Mail, Lock, User, Briefcase, Sparkles, LogIn, UserPlus } from "lucide-react";
import useAuth from "../hooks/useAuth";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Badge from "../components/common/Badge";
import "../styles/login.css";

function Login() {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [department, setDepartment] = useState("");
  const [designation, setDesignation] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (isRegister) {
        await register({ name, email, password, department, designation });
        alert("Registration successful! Please login.");
        setIsRegister(false);
      } else {
        await login(email, password);
        navigate("/dashboard");
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Authentication failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-shell">
      <div className="login-card-wrapper">
        <Card className="glass-card" style={{ padding: "40px" }}>
          {/* Logo & Brand */}
          <div style={{ textAlign: "center", marginBottom: "24px" }}>
            <div className="login-brand-icon">
              <BrainCircuit size={28} />
            </div>
            <Badge variant="purple" icon={Sparkles} style={{ marginTop: "12px" }}>
              Enterprise Edition 1.0
            </Badge>
            <h1 style={{ fontSize: "1.75rem", fontWeight: 800, marginTop: "10px" }}>
              AI Learning Platform
            </h1>
            <p style={{ fontSize: "0.9rem", color: "var(--text-muted)", marginTop: "4px" }}>
              Sign in to access your enterprise AI workspace
            </p>
          </div>

          {/* Toggle Switch */}
          <div className="login-toggle-bar">
            <button
              className={`login-toggle-btn ${!isRegister ? "active" : ""}`}
              onClick={() => setIsRegister(false)}
            >
              Sign In
            </button>
            <button
              className={`login-toggle-btn ${isRegister ? "active" : ""}`}
              onClick={() => setIsRegister(true)}
            >
              Register
            </button>
          </div>

          {error && <div className="login-error-banner">{error}</div>}

          <form onSubmit={handleSubmit}>
            {isRegister && (
              <>
                <div className="login-input-group">
                  <label>Full Name</label>
                  <div className="login-input-box">
                    <User size={18} color="var(--text-muted)" />
                    <input
                      type="text"
                      placeholder="Jane Doe"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      required
                    />
                  </div>
                </div>

                <div className="login-input-group">
                  <label>Department</label>
                  <div className="login-input-box">
                    <Briefcase size={18} color="var(--text-muted)" />
                    <input
                      type="text"
                      placeholder="Engineering"
                      value={department}
                      onChange={(e) => setDepartment(e.target.value)}
                      required
                    />
                  </div>
                </div>

                <div className="login-input-group">
                  <label>Designation</label>
                  <div className="login-input-box">
                    <Briefcase size={18} color="var(--text-muted)" />
                    <input
                      type="text"
                      placeholder="Backend Engineer"
                      value={designation}
                      onChange={(e) => setDesignation(e.target.value)}
                      required
                    />
                  </div>
                </div>
              </>
            )}

            <div className="login-input-group">
              <label>Email Address</label>
              <div className="login-input-box">
                <Mail size={18} color="var(--text-muted)" />
                <input
                  type="email"
                  placeholder="jane@company.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="login-input-group">
              <label>Password</label>
              <div className="login-input-box">
                <Lock size={18} color="var(--text-muted)" />
                <input
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
            </div>

            <Button
              type="submit"
              icon={isRegister ? UserPlus : LogIn}
              style={{ width: "100%", marginTop: "20px" }}
              disabled={loading}
            >
              {loading ? "Authenticating..." : isRegister ? "Create Account" : "Sign In to Platform"}
            </Button>
          </form>
        </Card>
      </div>
    </div>
  );
}

export default Login;