import React, { useState } from "react";
import { Bot, ChevronDown, ChevronUp, Wrench, Clock, ShieldCheck, Cpu } from "lucide-react";
import Badge from "./Badge";

export function AgentReasoningNode({ step, stepIndex }) {
  const [collapsed, setCollapsed] = useState(false);

  if (!step) return null;

  return (
    <div
      style={{
        background: "var(--bg-surface)",
        border: "1px solid var(--border-color)",
        borderRadius: "var(--radius-md)",
        padding: "16px 20px",
        marginBottom: "12px",
        boxShadow: "var(--shadow-sm)",
        transition: "all 0.2s ease",
      }}
    >
      {/* Node Header */}
      <div
        onClick={() => setCollapsed(!collapsed)}
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          cursor: "pointer",
          userSelect: "none",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <div
            style={{
              width: "34px",
              height: "34px",
              borderRadius: "var(--radius-sm)",
              background: "var(--color-primary-light)",
              color: "var(--color-primary)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: 700,
              fontSize: "0.9rem",
            }}
          >
            {stepIndex + 1}
          </div>

          <div>
            <h4 style={{ fontSize: "0.98rem", fontWeight: 700, color: "var(--text-primary)", display: "flex", alignItems: "center", gap: "6px" }}>
              <Bot size={16} color="var(--color-primary)" />
              {step.agent_name || "Specialized Agent"}
            </h4>
            <span style={{ fontSize: "0.78rem", color: "var(--text-muted)", display: "flex", alignItems: "center", gap: "8px", marginTop: "2px" }}>
              <span><Clock size={11} style={{ display: "inline", marginRight: "3px" }} />{step.execution_time_ms || 120} ms</span>
              <span>•</span>
              <span><ShieldCheck size={11} style={{ display: "inline", marginRight: "3px" }} />{step.confidence_score || 95}% Confidence</span>
            </span>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <Badge variant={step.confidence_score >= 90 ? "success" : "purple"}>
            {step.confidence_score >= 90 ? "Verified" : "Processing"}
          </Badge>
          <button
            style={{
              background: "none",
              border: "none",
              color: "var(--text-muted)",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
            }}
          >
            {collapsed ? <ChevronDown size={18} /> : <ChevronUp size={18} />}
          </button>
        </div>
      </div>

      {/* Node Body Details */}
      {!collapsed && (
        <div style={{ marginTop: "14px", paddingTop: "14px", borderTop: "1px solid var(--border-color)" }}>
          <p style={{ fontSize: "0.92rem", color: "var(--text-secondary)", lineHeight: 1.5, marginBottom: "10px" }}>
            {step.reasoning}
          </p>

          {/* Tool Calls Execution Badge */}
          {step.tool_calls && step.tool_calls.length > 0 && (
            <div
              style={{
                marginTop: "10px",
                padding: "10px 14px",
                borderRadius: "var(--radius-sm)",
                background: "rgba(16, 185, 129, 0.08)",
                border: "1px solid rgba(16, 185, 129, 0.2)",
                fontSize: "0.82rem",
                color: "var(--color-success)",
                display: "flex",
                alignItems: "center",
                gap: "8px",
              }}
            >
              <Wrench size={15} />
              <div>
                <strong>Tools Executed:</strong>{" "}
                {step.tool_calls.map((t) => t.tool_name || t).join(", ")}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default AgentReasoningNode;
