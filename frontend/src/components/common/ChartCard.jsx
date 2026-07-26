import React from "react";
import Card from "./Card";

export function ChartCard({ title, subtitle, children, action }) {
  return (
    <Card>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
        <div>
          <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--text-primary)" }}>{title}</h3>
          {subtitle && <p style={{ fontSize: "0.82rem", color: "var(--text-muted)", marginTop: "2px" }}>{subtitle}</p>}
        </div>
        {action && <div>{action}</div>}
      </div>

      <div style={{ width: "100%", height: "260px" }}>{children}</div>
    </Card>
  );
}

export default ChartCard;
