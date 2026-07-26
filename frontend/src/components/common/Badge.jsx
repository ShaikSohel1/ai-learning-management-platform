import React from "react";

export function Badge({ children, variant = "primary", icon: Icon, className = "" }) {
  const getBadgeStyles = () => {
    switch (variant) {
      case "success":
        return { background: "var(--color-success-light)", color: "var(--color-success)" };
      case "warning":
        return { background: "var(--color-warning-light)", color: "var(--color-warning)" };
      case "danger":
        return { background: "var(--color-danger-light)", color: "var(--color-danger)" };
      case "purple":
        return { background: "rgba(139, 92, 246, 0.15)", color: "var(--color-accent)" };
      default:
        return { background: "var(--color-primary-light)", color: "var(--color-primary)" };
    }
  };

  return (
    <span
      className={`ui-badge ${className}`}
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "4px",
        padding: "4px 10px",
        borderRadius: "var(--radius-full)",
        fontSize: "0.78rem",
        fontWeight: 700,
        lineHeight: 1,
        ...getBadgeStyles(),
      }}
    >
      {Icon && <Icon size={12} />}
      {children}
    </span>
  );
}

export default Badge;
