import React from "react";

export function SectionHeader({ title, subtitle, action }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "20px" }}>
      <div>
        <h2 className="text-section" style={{ color: "var(--text-primary)" }}>{title}</h2>
        {subtitle && (
          <p className="text-body" style={{ color: "var(--text-muted)", marginTop: "4px" }}>
            {subtitle}
          </p>
        )}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}

export default SectionHeader;
