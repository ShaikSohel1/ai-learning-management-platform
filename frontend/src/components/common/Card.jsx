import React from "react";
import { motion } from "framer-motion";

export function Card({
  children,
  className = "",
  style = {},
  onClick,
  variant = "default", // 'default' | 'glass' | 'hero' | 'glow' | 'outline'
  hoverEffect = true,
}) {
  const getVariantStyles = () => {
    switch (variant) {
      case "hero":
        return {
          background: "var(--bg-surface)",
          border: "1px solid var(--border-color-active)",
          boxShadow: "var(--shadow-surface)",
        };
      case "glow":
        return {
          background: "var(--bg-surface)",
          border: "1px solid var(--border-color-active)",
          boxShadow: "var(--shadow-glow)",
        };
      case "glass":
        return {
          background: "rgba(0, 0, 0, 0.75)",
          backdropFilter: "blur(16px)",
          WebkitBackdropFilter: "blur(16px)",
          border: "1px solid var(--border-color)",
        };
      case "outline":
        return {
          background: "transparent",
          border: "1px dashed var(--border-color-hover)",
        };
      default:
        return {
          background: "var(--bg-surface)",
          border: "1px solid var(--border-color)",
          boxShadow: "var(--shadow-sm)",
        };
    }
  };

  return (
    <motion.div
      whileHover={hoverEffect ? { y: -2, transition: { duration: 0.3, ease: [0.61, 1, 0.88, 1] } } : {}}
      onClick={onClick}
      className={`ui-card-container ${className}`}
      style={{
        borderRadius: "var(--radius-sm)",
        padding: "24px",
        cursor: onClick ? "pointer" : "default",
        color: "var(--text-primary)",
        ...getVariantStyles(),
        ...style,
      }}
    >
      {children}
    </motion.div>
  );
}

export default Card;
