import React from "react";

export function Button({
  children,
  variant = "primary", // primary | secondary | outline | danger | ghost
  size = "md", // sm | md | lg
  icon: Icon,
  disabled = false,
  onClick,
  className = "",
  type = "button",
  style = {},
}) {
  const getVariantStyles = () => {
    switch (variant) {
      case "primary":
        return {
          background: "var(--color-primary)",
          color: "#ffffff",
          border: "none",
        };
      case "secondary":
        return {
          background: "var(--color-primary-light)",
          color: "var(--color-primary)",
          border: "none",
        };
      case "outline":
        return {
          background: "transparent",
          color: "var(--text-primary)",
          border: "1px solid var(--border-color)",
        };
      case "danger":
        return {
          background: "var(--color-danger-light)",
          color: "var(--color-danger)",
          border: "none",
        };
      case "ghost":
        return {
          background: "transparent",
          color: "var(--text-secondary)",
          border: "none",
        };
      default:
        return {};
    }
  };

  const getSizeStyles = () => {
    switch (size) {
      case "sm":
        return { padding: "6px 14px", fontSize: "0.82rem", borderRadius: "var(--radius-sm)" };
      case "lg":
        return { padding: "14px 28px", fontSize: "1rem", borderRadius: "var(--radius-md)" };
      default:
        return { padding: "10px 20px", fontSize: "0.9rem", borderRadius: "var(--radius-md)" };
    }
  };

  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      className={`ui-btn ${className}`}
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "8px",
        fontWeight: 600,
        cursor: disabled ? "not-allowed" : "pointer",
        opacity: disabled ? 0.6 : 1,
        transition: "all 0.2s ease",
        fontFamily: "var(--font-sans)",
        ...getVariantStyles(),
        ...getSizeStyles(),
        ...style,
      }}
    >
      {Icon && <Icon size={size === "sm" ? 16 : 18} />}
      {children}
    </button>
  );
}

export default Button;
