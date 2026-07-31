import React from "react";

export function PasswordStrengthMeter({ password = "" }) {
  const calculateStrength = (pass) => {
    let score = 0;
    if (!pass) return { score: 0, label: "", color: "transparent", percent: 0 };

    if (pass.length >= 8) score += 1;
    if (/[a-z]/.test(pass) && /[A-Z]/.test(pass)) score += 1;
    if (/\d/.test(pass)) score += 1;
    if (/[^a-zA-Z0-9]/.test(pass)) score += 1;

    switch (score) {
      case 1:
        return { score: 1, label: "Weak", color: "#EF4444", percent: 25 };
      case 2:
        return { score: 2, label: "Fair", color: "#F59E0B", percent: 50 };
      case 3:
        return { score: 3, label: "Good", color: "#3B82F6", percent: 75 };
      case 4:
        return { score: 4, label: "Strong", color: "#10B981", percent: 100 };
      default:
        return { score: 0, label: "Too Short", color: "#EF4444", percent: 10 };
    }
  };

  const strength = calculateStrength(password);

  if (!password) return null;

  return (
    <div style={{ marginTop: "8px", marginBottom: "16px" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: "0.78rem",
          color: "var(--text-muted, #94A3B8)",
          marginBottom: "6px",
        }}
      >
        <span>Password Strength:</span>
        <span style={{ color: strength.color, fontWeight: 600 }}>{strength.label}</span>
      </div>
      <div
        style={{
          height: "6px",
          width: "100%",
          backgroundColor: "rgba(255, 255, 255, 0.1)",
          borderRadius: "3px",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${strength.percent}%`,
            backgroundColor: strength.color,
            borderRadius: "3px",
            transition: "all 0.3s ease",
          }}
        />
      </div>
    </div>
  );
}

export default PasswordStrengthMeter;
