import { useState } from "react";
import Navbar from "../components/Navbar";
import agentService from "../services/agentService";
import enrollmentService from "../services/enrollmentService";
import "../styles/aiAssistant.css";

function AIAssistant() {
  const [activeTab, setActiveTab] = useState("agents");

  const [goalQuery, setGoalQuery] = useState("");
  const [loadingAgent, setLoadingAgent] = useState(false);
  const [agentResponse, setAgentResponse] = useState(null);
  const [agentError, setAgentError] = useState("");
  const [actionSuccess, setActionSuccess] = useState("");

  const handleRunAgentWorkflow = async (queryText) => {
    const q = queryText || goalQuery;
    if (!q.trim()) return;

    setLoadingAgent(true);
    setAgentError("");
    setActionSuccess("");
    setAgentResponse(null);

    try {
      const res = await agentService.sendAgentChat({
        message: q.trim(),
        career_goal: q.trim(),
        current_skills: ["Python", "HTML", "Git"],
      });
      setAgentResponse(res);
    } catch (err) {
      console.error("Agent execution error:", err);
      setAgentError(
        err.response?.data?.detail || "Failed to execute agentic workflow."
      );
    } finally {
      setLoadingAgent(false);
    }
  };

  const handleExecuteRecommendedAction = async (action) => {
    if (!action || !action.course_id) return;

    try {
      await enrollmentService.enrollUser(action.course_id);
      setActionSuccess(`Successfully enrolled in "${action.course_title}"! Check your 'My Learning' tab.`);
    } catch (err) {
      alert(err.response?.data?.detail || "Could not complete course enrollment.");
    }
  };

  // 1-Click Calendar Export Action
  const handleExportCalendar = () => {
    const token = localStorage.getItem("token");
    window.open(`http://127.0.0.1:8000/agents/calendar/export-ics?course_title=Backend%20Architecture&token=${token}`, "_blank");
    setActionSuccess("Downloading iCalendar (.ics) study schedule!");
  };

  // 1-Click Report CSV Action
  const handleExportProgressReport = () => {
    const token = localStorage.getItem("token");
    window.open(`http://127.0.0.1:8000/agents/reports/progress-csv?token=${token}`, "_blank");
    setActionSuccess("Downloading Learning Progress CSV Report!");
  };

  return (
    <div>
      <Navbar />

      <div className="ai-container">
        <div className="ai-header">
          <h1>⚡ Enterprise AI Action Assistant</h1>
          <p>
            Autonomous specialized AI agents executing real tool actions across course enrollments, study schedules, notifications, and analytics reports.
          </p>
        </div>

        <div className="ai-tabs">
          <button
            className={`ai-tab-btn ${activeTab === "agents" ? "active" : ""}`}
            onClick={() => setActiveTab("agents")}
          >
            🤖 Enterprise AI Action Platform
          </button>
          <button
            className={`ai-tab-btn ${activeTab === "chat" ? "active" : ""}`}
            onClick={() => setActiveTab("chat")}
          >
            💬 Direct Assistant Chat
          </button>
        </div>

        {activeTab === "agents" && (
          <div>
            <div className="ai-card">
              <h2 style={{ fontSize: "1.25rem", fontWeight: 700, marginBottom: "15px" }}>
                🎯 State Your Career Goal or Tool Execution Instruction
              </h2>

              {actionSuccess && <div className="success-banner">{actionSuccess}</div>}
              {agentError && <div className="error-banner">{agentError}</div>}

              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleRunAgentWorkflow();
                }}
              >
                <div className="form-group">
                  <div style={{ display: "flex", gap: "10px" }}>
                    <input
                      type="text"
                      className="form-control"
                      placeholder="e.g. 'I want to become a Backend Developer' or 'Enroll me in Python'"
                      value={goalQuery}
                      onChange={(e) => setGoalQuery(e.target.value)}
                      required
                    />
                    <button
                      type="submit"
                      className="btn-ai-primary"
                      style={{ width: "auto", padding: "0 28px", whiteSpace: "nowrap" }}
                      disabled={loadingAgent}
                    >
                      {loadingAgent ? "Executing Actions..." : "Execute AI Tools"}
                    </button>
                  </div>
                </div>
              </form>

              {/* 1-Click Action Preset Toolbar */}
              <div style={{ marginTop: "20px" }}>
                <h4 style={{ fontSize: "0.9rem", color: "#475569", marginBottom: "10px" }}>
                  ⚡ 1-Click Enterprise Action Triggers:
                </h4>
                <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                  <button
                    type="button"
                    className="knowledge-tab-btn"
                    style={{ background: "#f0fdf4", borderColor: "#86efac", color: "#166534" }}
                    onClick={() => {
                      setGoalQuery("Enroll me in course 1 and send notification");
                      handleRunAgentWorkflow("Enroll me in course 1 and send notification");
                    }}
                  >
                    🎓 Enroll in Course 1
                  </button>

                  <button
                    type="button"
                    className="knowledge-tab-btn"
                    style={{ background: "#eff6ff", borderColor: "#93c5fd", color: "#1e40af" }}
                    onClick={handleExportCalendar}
                  >
                    📅 Export Study Plan (.ics)
                  </button>

                  <button
                    type="button"
                    className="knowledge-tab-btn"
                    style={{ background: "#fef3c7", borderColor: "#fde047", color: "#854d0e" }}
                    onClick={handleExportProgressReport}
                  >
                    📊 Export Progress CSV Report
                  </button>

                  <button
                    type="button"
                    className="knowledge-tab-btn"
                    style={{ background: "#f3e8ff", borderColor: "#d8b4fe", color: "#6b21a8" }}
                    onClick={() => {
                      setGoalQuery("Assess my skills for Senior Developer role");
                      handleRunAgentWorkflow("Assess my skills for Senior Developer role");
                    }}
                  >
                    📝 Skill Assessment Tool
                  </button>
                </div>
              </div>
            </div>

            {loadingAgent && (
              <div className="ai-card">
                <div className="loading-pulse">
                  <div className="pulse-dot"></div>
                  <div className="pulse-dot"></div>
                  <div className="pulse-dot"></div>
                  <span>Running Tool Executions (Planning ➔ Searching ➔ Tool Calling ➔ Completed)...</span>
                </div>
              </div>
            )}

            {agentResponse && !loadingAgent && (
              <div className="ai-card">
                <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "15px" }}>
                  🔄 Agent Tool Execution Timeline
                </h3>

                <div className="pipeline-timeline">
                  {agentResponse.steps.map((step, idx) => (
                    <div key={idx} className="pipeline-step completed">
                      <div className="pipeline-node">✓</div>
                      <div className="pipeline-label">{step.agent_name.replace(" Agent", "")}</div>
                    </div>
                  ))}
                </div>

                <div className="rag-header-meta" style={{ marginBottom: "20px" }}>
                  <span className="rag-header-badge badge-confidence">
                    Overall Confidence: {agentResponse.overall_confidence}%
                  </span>
                  <span className="rag-header-badge badge-latency">
                    ⚡ Total Latency: {agentResponse.total_execution_time_ms} ms
                  </span>
                  <span className="rag-header-badge badge-intent">
                    🎯 Intent: {agentResponse.workflow_intent}
                  </span>
                </div>

                <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "15px" }}>
                  🛠️ Tool Calling & Execution Log ({agentResponse.steps.length})
                </h3>

                {agentResponse.steps.map((step, idx) => (
                  <div key={idx} className="agent-step-card">
                    <div className="agent-step-head">
                      <div className="agent-name-badge">
                        🤖 {step.agent_name}
                      </div>
                      <div>
                        <span className="agent-meta-badge">{step.confidence_score}% Confidence</span>
                        <span className="agent-meta-badge" style={{ marginLeft: "6px" }}>{step.execution_time_ms} ms</span>
                      </div>
                    </div>

                    <div className="agent-reasoning-text">{step.reasoning}</div>

                    {step.tool_calls?.length > 0 && (
                      <div style={{ marginTop: "10px", fontSize: "0.82rem", color: "#047857", background: "#f0fdf4", padding: "8px 12px", borderRadius: "6px" }}>
                        🛠️ <strong>Tool Executed:</strong> {step.tool_calls.map(t => t.tool_name).join(", ")}
                      </div>
                    )}
                  </div>
                ))}

                <div className="rag-answer-box" style={{ marginTop: "25px" }}>
                  <h3 style={{ fontSize: "1.15rem", fontWeight: 700, color: "#1e3a8a", marginBottom: "10px" }}>
                    📋 Executive Orchestrator Final Response
                  </h3>
                  <div className="rag-answer-text">{agentResponse.final_summary}</div>
                </div>

                {agentResponse.recommended_action && (
                  <div className="executable-action-box">
                    <div>
                      <div className="executable-action-title">
                        ⚡ Recommended Action Ready for Execution
                      </div>
                      <div style={{ fontSize: "0.88rem", color: "#047857", marginTop: "2px" }}>
                        {agentResponse.recommended_action.course_title}
                      </div>
                    </div>

                    <button
                      className="btn-action-execute"
                      onClick={() => handleExecuteRecommendedAction(agentResponse.recommended_action)}
                    >
                      {agentResponse.recommended_action.label}
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {activeTab === "chat" && (
          <div className="ai-card">
            <h2 style={{ fontSize: "1.2rem", fontWeight: 700, marginBottom: "15px" }}>
              💬 Direct Assistant Chat
            </h2>
            <p style={{ color: "#64748b" }}>
              Use the Enterprise AI Action Platform tab above for autonomous tool execution.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default AIAssistant;
