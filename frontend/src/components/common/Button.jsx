import React from "react";
import { motion } from "framer-motion";

export function Button({
  children,
  variant = "primary", // primary | secondary | outline | danger | ghost | glow
  size = "md", // sm | md | lg
  icon: Icon,
  disabled = false,
  loading = false,
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
          color: "var(--text-inverse)",
          border: "none",
          boxShadow: "var(--glow-cta)",
        };
      case "glow":
        return {
          background: "var(--color-primary)",
          color: "var(--text-inverse)",
          border: "1px solid rgba(228, 181, 146, 0.3)",
          boxShadow: "0 0 20px rgba(228, 181, 146, 0.25)",
        };
      case "secondary":
        return {
          background: "var(--color-primary-light)",
          color: "var(--color-primary)",
          border: "1px solid rgba(228, 181, 146, 0.2)",
        };
      case "outline":
        return {
          background: "var(--bg-surface)",
          color: "var(--text-primary)",
          border: "1px solid var(--border-color)",
        };
      case "danger":
        return {
          background: "var(--color-danger-light)",
          color: "var(--color-danger)",
          border: "1px solid rgba(248, 113, 113, 0.2)",
        };
      case "ghost":
        return {
          background: "transparent",
          color: "var(--text-on-cream-muted)",
          border: "none",
        };
      default:
        return {};
    }
  };

  const getSizeStyles = () => {
    switch (size) {
      case "sm":
        return { padding: "7px 14px", fontSize: "13px", borderRadius: "var(--radius-sm)" };
      case "lg":
        return { padding: "14px 28px", fontSize: "16px", borderRadius: "var(--radius-sm)" };
      default:
        return { padding: "10px 20px", fontSize: "14px", borderRadius: "var(--radius-sm)" };
    }
  };

  return (
    <motion.button
      whileHover={{ scale: disabled || loading ? 1 : 1.02 }}
      whileTap={{ scale: disabled || loading ? 1 : 0.97 }}
      transition={{ duration: 0.15 }}
      type={type}
      disabled={disabled || loading}
      onClick={onClick}
      className={`ui-btn ${className}`}
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "8px",
        fontWeight: 700,
        letterSpacing: "-0.01em",
        cursor: disabled || loading ? "not-allowed" : "pointer",
        opacity: disabled || loading ? 0.65 : 1,
        fontFamily: "var(--font-sans)",
        transition: "background 0.3s cubic-bezier(0.61,1,0.88,1), border-color 0.3s cubic-bezier(0.61,1,0.88,1), box-shadow 0.3s cubic-bezier(0.61,1,0.88,1)",
        ...getVariantStyles(),
        ...getSizeStyles(),
        ...style,
      }}
    >
      {loading ? (
        <span style={{ display: "inline-block", width: 14, height: 14, border: "2px solid currentColor", borderTopColor: "transparent", borderRadius: "50%", animation: "spin 0.8s linear infinite" }} />
      ) : Icon ? (
        <Icon size={size === "sm" ? 15 : size === "lg" ? 20 : 17} />
      ) : null}
      {children}
    </motion.button>
  );
}

export default Button;
