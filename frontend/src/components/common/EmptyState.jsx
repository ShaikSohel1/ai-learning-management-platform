import React from "react";
import Button from "./Button";

export function EmptyState({ icon: Icon, title, description, actionLabel, onAction }) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "48px 24px",
        textAlign: "center",
        borderRadius: "var(--radius-lg)",
        background: "var(--bg-surface)",
        border: "1px dashed var(--border-color)",
      }}
    >
      {Icon && (
        <div
          style={{
            width: "56px",
            height: "56px",
            borderRadius: "50%",
            background: "var(--color-primary-light)",
            color: "var(--color-primary)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            marginBottom: "16px",
          }}
        >
          <Icon size={28} />
        </div>
      )}
      <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--text-primary)" }}>{title}</h3>
      {description && (
        <p style={{ fontSize: "0.88rem", color: "var(--text-secondary)", maxWidth: "420px", marginTop: "6px" }}>
          {description}
        </p>
      )}
      {actionLabel && onAction && (
        <div style={{ marginTop: "20px" }}>
          <Button onClick={onAction}>{actionLabel}</Button>
        </div>
      )}
    </div>
  );
}

export default EmptyState;
