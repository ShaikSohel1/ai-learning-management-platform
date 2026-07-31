import React, { useEffect } from "react";
import { CheckCircle2, AlertCircle, Info, X } from "lucide-react";

export function ToastNotification({ message, type = "success", onClose, duration = 5000 }) {
  useEffect(() => {
    if (!message) return;
    const timer = setTimeout(() => {
      if (onClose) onClose();
    }, duration);
    return () => clearTimeout(timer);
  }, [message, duration, onClose]);

  if (!message) return null;

  const icons = {
    success: <CheckCircle2 size={18} color="#10B981" />,
    error: <AlertCircle size={18} color="#EF4444" />,
    info: <Info size={18} color="#3B82F6" />,
  };

  const bgColors = {
    success: "rgba(16, 185, 129, 0.12)",
    error: "rgba(239, 68, 68, 0.12)",
    info: "rgba(59, 130, 246, 0.12)",
  };

  const borderColors = {
    success: "rgba(16, 185, 129, 0.3)",
    error: "rgba(239, 68, 68, 0.3)",
    info: "rgba(59, 130, 246, 0.3)",
  };

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justify: "space-between",
        gap: "12px",
        padding: "12px 16px",
        borderRadius: "10px",
        background: bgColors[type] || bgColors.info,
        border: `1px solid ${borderColors[type] || borderColors.info}`,
        backdropFilter: "blur(8px)",
        color: "var(--text-primary, #F8FAFC)",
        fontSize: "0.88rem",
        boxShadow: "0 8px 20px rgba(0,0,0,0.25)",
        marginBottom: "16px",
        animation: "fadeIn 0.3s ease-out",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
        {icons[type] || icons.info}
        <span>{message}</span>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          type="button"
          style={{
            background: "transparent",
            border: "none",
            color: "var(--text-muted, #94A3B8)",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            padding: "2px",
          }}
        >
          <X size={16} />
        </button>
      )}
    </div>
  );
}

export default ToastNotification;
