import React from "react";
import { motion } from "framer-motion";
import Card from "./Card";

export function MetricCard({ title, value, icon: Icon, trend, color = "purple", description }) {
  const getColorStyle = () => {
    switch (color) {
      case "emerald":
        return { bg: "var(--color-success-light)", iconColor: "var(--color-success)" };
      case "indigo":
        return { bg: "rgba(99, 102, 241, 0.12)", iconColor: "var(--color-secondary)" };
      case "amber":
        return { bg: "var(--color-warning-light)", iconColor: "var(--color-warning)" };
      case "rose":
        return { bg: "var(--color-danger-light)", iconColor: "var(--color-danger)" };
      default:
        return { bg: "var(--color-primary-light)", iconColor: "var(--color-primary)" };
    }
  };

  const palette = getColorStyle();

  return (
    <Card style={{ position: "relative" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <span className="text-caption" style={{ fontWeight: 600, color: "var(--text-secondary)" }}>
            {title}
          </span>
          <div style={{ fontSize: "1.85rem", fontWeight: 800, marginTop: "6px", color: "var(--text-primary)", letterSpacing: "-0.02em" }}>
            {value}
          </div>
        </div>

        {Icon && (
          <div
            style={{
              width: "44px",
              height: "44px",
              borderRadius: "var(--radius-md)",
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

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginTop: "14px" }}>
        <div>
          {trend && (
            <span style={{ fontSize: "0.78rem", fontWeight: 700, color: "var(--color-success)" }}>
              {trend}
            </span>
          )}
          {description && (
            <div className="text-caption" style={{ marginTop: "2px" }}>
              {description}
            </div>
          )}
        </div>

        {/* Tiny Sparkline Wave */}
        <svg width="60" height="24" viewBox="0 0 60 24" fill="none">
          <path
            d="M2 18 C 15 8, 25 22, 38 10 C 48 2, 52 14, 58 6"
            stroke={palette.iconColor}
            strokeWidth="2.5"
            strokeLinecap="round"
          />
        </svg>
      </div>
    </Card>
  );
}

export default MetricCard;
