import React from "react";
import Card from "./Card";

export function StatCard({ title, value, icon: Icon, trend, color = "indigo", description }) {
  const getColorStyle = () => {
    switch (color) {
      case "emerald":
        return { bg: "rgba(34, 197, 94, 0.12)", iconColor: "#22c55e" };
      case "purple":
        return { bg: "rgba(139, 92, 246, 0.12)", iconColor: "#8b5cf6" };
      case "amber":
        return { bg: "rgba(245, 158, 11, 0.12)", iconColor: "#f59e0b" };
      case "rose":
        return { bg: "rgba(239, 68, 68, 0.12)", iconColor: "#ef4444" };
      default:
        return { bg: "rgba(99, 102, 241, 0.12)", iconColor: "#6366f1" };
    }
  };

  const palette = getColorStyle();

  return (
    <Card style={{ position: "relative", overflow: "hidden" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <span style={{ fontSize: "0.85rem", fontWeight: 600, color: "var(--text-secondary)" }}>
            {title}
          </span>
          <div style={{ fontSize: "1.8rem", fontWeight: 800, marginTop: "6px", color: "var(--text-primary)" }}>
            {value}
          </div>
          {description && (
            <div style={{ fontSize: "0.78rem", color: "var(--text-muted)", marginTop: "4px" }}>
              {description}
            </div>
          )}
        </div>

        {Icon && (
          <div
            style={{
              width: "48px",
              height: "48px",
              borderRadius: "var(--radius-md)",
              background: palette.bg,
              color: palette.iconColor,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Icon size={24} />
          </div>
        )}
      </div>

      {trend && (
        <div style={{ marginTop: "12px", fontSize: "0.8rem", fontWeight: 600, color: "var(--color-success)" }}>
          {trend}
        </div>
      )}
    </Card>
  );
}

export default StatCard;
