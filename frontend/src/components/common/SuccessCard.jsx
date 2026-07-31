import React from "react";
import { CheckCircle2, ArrowRight } from "lucide-react";
import Button from "./Button";
import Card from "./Card";

export function SuccessCard({ title, description, actionText = "Back to Sign In", onAction }) {
  return (
    <Card variant="glass" style={{ padding: "36px", textAlign: "center" }}>
      <div
        style={{
          width: "56px",
          height: "56px",
          borderRadius: "50%",
          background: "rgba(16, 185, 129, 0.15)",
          border: "1px solid rgba(16, 185, 129, 0.3)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          margin: "0 auto 20px auto",
        }}
      >
        <CheckCircle2 size={32} color="#10B981" />
      </div>

      <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "10px", color: "var(--text-primary)" }}>
        {title}
      </h2>

      <p style={{ fontSize: "0.92rem", color: "var(--text-muted)", marginBottom: "24px", lineHeight: "1.5" }}>
        {description}
      </p>

      {onAction && (
        <Button variant="glow" icon={ArrowRight} onClick={onAction} style={{ width: "100%" }}>
          {actionText}
        </Button>
      )}
    </Card>
  );
}

export default SuccessCard;
