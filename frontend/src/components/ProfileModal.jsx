import React from "react";
import { User, Mail, Briefcase, Target, ShieldCheck, X, Sparkles } from "lucide-react";
import useAuth from "../hooks/useAuth";
import Button from "./common/Button";
import Badge from "./common/Badge";

export function ProfileModal({ isOpen, onClose }) {
  const { user } = useAuth();

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
        style={{ maxWidth: "480px" }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            <div
              style={{
                width: "44px",
                height: "44px",
                borderRadius: "50%",
                background: "var(--gradient-cta)",
                color: "white",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontWeight: 800,
                fontSize: "1.2rem",
              }}
            >
              {user?.name ? user.name[0].toUpperCase() : "U"}
            </div>
            <div>
              <h3 style={{ fontSize: "1.15rem", fontWeight: 800 }}>{user?.name || "Learner User"}</h3>
              <span style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>{user?.email || "user@company.com"}</span>
            </div>
          </div>

          <button
            onClick={onClose}
            style={{ background: "none", border: "none", color: "var(--text-muted)", cursor: "pointer" }}
          >
            <X size={20} />
          </button>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginBottom: "24px" }}>
          <div style={{ background: "var(--bg-surface-elevated)", padding: "12px 16px", borderRadius: "var(--radius-md)", border: "1px solid var(--border-color)" }}>
            <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", fontWeight: 600, display: "block" }}>Role & Permission</span>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: "4px" }}>
              <strong style={{ fontSize: "0.95rem" }}>{user?.role || "STUDENT"}</strong>
              <Badge variant="purple" icon={ShieldCheck}>Verified JWT</Badge>
            </div>
          </div>

          <div style={{ background: "var(--bg-surface-elevated)", padding: "12px 16px", borderRadius: "var(--radius-md)", border: "1px solid var(--border-color)" }}>
            <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", fontWeight: 600, display: "block" }}>Department & Designation</span>
            <div style={{ fontSize: "0.95rem", fontWeight: 700, marginTop: "4px", display: "flex", alignItems: "center", gap: "6px" }}>
              <Briefcase size={16} color="var(--color-primary)" />
              {user?.designation || "Senior Software Engineer"} • {user?.department || "Engineering"}
            </div>
          </div>

          <div style={{ background: "var(--bg-surface-elevated)", padding: "12px 16px", borderRadius: "var(--radius-md)", border: "1px solid var(--border-color)" }}>
            <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", fontWeight: 600, display: "block" }}>Target Career Pathway</span>
            <div style={{ fontSize: "0.95rem", fontWeight: 700, marginTop: "4px", color: "var(--color-success)", display: "flex", alignItems: "center", gap: "6px" }}>
              <Target size={16} />
              Senior Backend Architect (88% Match)
            </div>
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <Button onClick={onClose} variant="primary">
            Close Profile
          </Button>
        </div>
      </div>
    </div>
  );
}

export default ProfileModal;
