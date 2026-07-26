import React from "react";

export function LoadingSkeleton({ height = "120px", count = 1 }) {
  const items = Array.from({ length: count });

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "100%" }}>
      {items.map((_, i) => (
        <div
          key={i}
          style={{
            height,
            width: "100%",
            borderRadius: "var(--radius-md)",
            background: "linear-gradient(90deg, var(--border-color) 25%, var(--bg-surface-hover) 50%, var(--border-color) 75%)",
            backgroundSize: "200% 100%",
            animation: "skeleton-loading 1.5s infinite ease-in-out",
          }}
        />
      ))}
      <style>{`
        @keyframes skeleton-loading {
          0% { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
      `}</style>
    </div>
  );
}

export default LoadingSkeleton;
