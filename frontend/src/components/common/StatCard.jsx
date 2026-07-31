import React from "react";
import Card from "./Card";

export function StatCard({ title, value, icon: Icon, trend, color = "indigo", description }) {
  const getColorStyle = () => {
    switch (color) {
      case "emerald":
        return { bg: "var(--color-success-bg)", iconColor: "var(--color-success)" };
      case "purple":
        return { bg: "var(--color-primary-light)", iconColor: "var(--color-primary)" };
      case "amber":
        return { bg: "var(--color-warning-bg)", iconColor: "var(--color-warning)" };
      case "rose":
        return { bg: "var(--color-danger-bg)", iconColor: "var(--color-danger)" };
      default:
        return { bg: "var(--color-primary-light)", iconColor: "var(--color-primary)" };

    }
  };

  const palette = getColorStyle();

  return (
    <Card style={{ position: "relative", overflow: "hidden" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <span style={{ fontFamily: "var(--font-mono)", fontSize: "10px", fontWeight: 400, color: "var(--text-secondary)", letterSpacing: "-0.1px" }}>
            {title}
          </span>
          <div style={{ fontSize: "1.6rem", fontWeight: 700, marginTop: "6px", color: "var(--text-primary)" }}>
            {value}
          </div>
          {description && (
            <div style={{ fontSize: "0.72rem", color: "var(--text-muted)", marginTop: "4px", fontWeight: 600 }}>
              {description}
            </div>
          )}
        </div>

        {Icon && (
          <div
            style={{
              width: "44px",
              height: "44px",
              borderRadius: "var(--radius-sm)",
              background: palette.bg,
              color: palette.iconColor,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Icon size={22} />
          </div>
        )}
      </div>

      {trend && (
        <div style={{ marginTop: "12px", fontFamily: "var(--font-mono)", fontSize: "10px", fontWeight: 400, color: "var(--color-success)", letterSpacing: "-0.1px" }}>
          {trend}
        </div>
      )}
    </Card>
  );
}

export default StatCard;
