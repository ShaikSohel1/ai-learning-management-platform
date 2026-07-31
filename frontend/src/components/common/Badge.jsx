import React from "react";

export function Badge({ children, variant = "primary", icon: Icon, className = "", style = {} }) {
  const getBadgeStyles = () => {
    switch (variant) {
      case "success":
      case "emerald":
        return {
          background: "var(--color-success-light)",
          color: "var(--color-success)",
          border: "1px solid rgba(74, 222, 128, 0.25)",
        };
      case "warning":
      case "amber":
        return {
          background: "var(--color-warning-light)",
          color: "var(--color-warning)",
          border: "1px solid rgba(251, 191, 36, 0.25)",
        };
      case "danger":
      case "rose":
        return {
          background: "var(--color-danger-light)",
          color: "var(--color-danger)",
          border: "1px solid rgba(248, 113, 113, 0.25)",
        };
      case "purple":
      case "indigo":
        return {
          background: "var(--color-primary-light)",
          color: "var(--color-primary)",
          border: "1px solid rgba(228, 181, 146, 0.3)",
        };
      case "outline":
        return {
          background: "transparent",
          color: "var(--text-secondary)",
          border: "1px solid var(--border-color)",
        };
      case "glow":
        return {
          background: "var(--color-primary)",
          color: "var(--text-inverse)",
          border: "none",
          boxShadow: "0 0 12px rgba(228, 181, 146, 0.3)",
        };
      default:
        return {
          background: "var(--color-primary-light)",
          color: "var(--color-primary)",
          border: "1px solid rgba(228, 181, 146, 0.2)",
        };
    }
  };

  return (
    <span
      className={`ui-badge ${className}`}
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "5px",
        padding: "4px 10px",
        borderRadius: "var(--radius-full)",
        fontFamily: "var(--font-mono)",
        fontSize: "10px",
        fontWeight: 400,
        letterSpacing: "-0.1px",
        lineHeight: 1.2,
        ...getBadgeStyles(),
        ...style,
      }}
    >
      {Icon && <Icon size={12} />}
      {children}
    </span>
  );
}

export default Badge;
