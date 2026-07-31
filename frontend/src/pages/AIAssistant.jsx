import React, { useState, useEffect } from "react";
import {
  Sparkles,
  Bot,
  MessageSquare,
  Send,
  Cpu,
  CheckCircle2,
  Clock,
  Wrench,
  Zap,
  Terminal,
  Copy,
  Download,
  Trash2,
  ShieldCheck,
  PlayCircle,
  FileSpreadsheet,
  CalendarCheck,
} from "lucide-react";

import AppLayout from "../components/AppLayout";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Badge from "../components/common/Badge";
import MarkdownRenderer from "../components/common/MarkdownRenderer";
import AgentReasoningNode from "../components/common/AgentReasoningNode";
import agentService from "../services/agentService";
import enrollmentService from "../services/enrollmentService";
import systemService from "../services/systemService";
import "../styles/aiAssistant.css";

const chatSuggestions = [
  "Explain Python async/await principles",
  "Design a PostgreSQL database schema for LMS",
  "Summarize key enterprise leave policies",
  "How to implement JWT authentication in FastAPI?",
];

function AIAssistant() {
  const [activeTab, setActiveTab] = useState("agents");
  const [systemInfo, setSystemInfo] = useState({
    provider: "Google Gemini",
    model: "models/gemini-2.0-flash",
    status: "Operational",
  });


  useEffect(() => {
    systemService.getSystemInfo().then(setSystemInfo).catch(() => {});
  }, []);

  // Agentic Platform State
  const [goalQuery, setGoalQuery] = useState("");
  const [loadingAgent, setLoadingAgent] = useState(false);
  const [agentResponse, setAgentResponse] = useState(null);
  const [agentError, setAgentError] = useState("");
  const [actionSuccess, setActionSuccess] = useState("");

  // ChatGPT Chat State
  const [chatMessages, setChatMessages] = useState([
    {
      sender: "ai",
      text: "Hello! I am your Enterprise AI Assistant powered by Google Gemini. How can I assist your career development, technical questions, or policy search today?",
      timestamp: "10:00 AM",
    },
  ]);
  const [inputChat, setInputChat] = useState("");
  const [loadingChat, setLoadingChat] = useState(false);

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

  const handleSendDirectChat = async (textToSubmit) => {
    const text = textToSubmit || inputChat;
    if (!text.trim()) return;

    const userMsg = {
      sender: "user",
      text: text.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setChatMessages((prev) => [...prev, userMsg]);
    if (!textToSubmit) setInputChat("");
    setLoadingChat(true);

    try {
      const res = await agentService.sendAgentChat({
        message: text.trim(),
      });

      const aiMsg = {
        sender: "ai",
        text: res.final_summary,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setChatMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error("Chat error:", err);
    } finally {
      setLoadingChat(false);
    }
  };

  const handleExecuteRecommendedAction = async (action) => {
    if (!action || !action.course_id) return;

    try {
      await enrollmentService.enrollInCourse(action.course_id);
      setActionSuccess(`Successfully enrolled in "${action.course_title}"! Check your 'My Learning' tab.`);
    } catch (err) {
      alert(err.response?.data?.detail || "Could not complete course enrollment.");
    }
  };

  const handleExportCalendar = () => {
    const token = localStorage.getItem("token");
    window.open(`http://127.0.0.1:8000/agents/calendar/export-ics?course_title=Backend%20Architecture&token=${token}`, "_blank");
    setActionSuccess("Downloading iCalendar (.ics) study schedule!");
  };

  const handleExportProgressReport = () => {
    const token = localStorage.getItem("token");
    window.open(`http://127.0.0.1:8000/agents/reports/progress-csv?token=${token}`, "_blank");
    setActionSuccess("Downloading Learning Progress CSV Report!");
  };

  return (
    <AppLayout>
      <div className="ai-container">
        {/* Top Hero Banner */}
        <div className="ai-hero-banner">
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <Badge variant="glow" icon={Sparkles}>
                Enterprise Multi-Agent Engine
              </Badge>
              <Badge variant="success">{systemService.formatModelName(systemInfo.model)} Active</Badge>
            </div>
            <h1>Your Enterprise AI Assistant</h1>
            <p>
              Autonomous specialized AI agents collaborating to analyze skills, generate roadmaps, execute tool actions, and verify readiness.
            </p>
          </div>

          <div style={{ display: "flex", gap: "10px" }}>
            <Button
              variant={activeTab === "agents" ? "glow" : "outline"}
              icon={Bot}
              onClick={() => setActiveTab("agents")}
            >
              Multi-Agent Engine
            </Button>
            <Button
              variant={activeTab === "chat" ? "glow" : "outline"}
              icon={MessageSquare}
              onClick={() => setActiveTab("chat")}
            >
              ChatGPT Stream
            </Button>
          </div>
        </div>

        {/* Tab 1: Multi-Agent Engine */}
        {activeTab === "agents" && (
          <div>
            <Card style={{ marginBottom: "24px" }}>
              <h2 style={{ fontSize: "1.15rem", fontWeight: 700, marginBottom: "14px", display: "flex", alignItems: "center", gap: "8px" }}>
                <Cpu size={20} color="var(--color-primary)" /> State Your Career Goal or Execution Instruction
              </h2>

              {actionSuccess && <div className="success-banner">{actionSuccess}</div>}
              {agentError && <div className="error-banner">{agentError}</div>}

              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleRunAgentWorkflow();
                }}
              >
                <div style={{ display: "flex", gap: "12px" }}>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="e.g. 'I want to become a Senior Backend Developer' or 'Enroll me in Python course'"
                    value={goalQuery}
                    onChange={(e) => setGoalQuery(e.target.value)}
                    required
                  />
                  <Button type="submit" icon={Cpu} loading={loadingAgent} variant="glow">
                    Execute Agents
                  </Button>
                </div>
              </form>

              {/* 1-Click Action Preset Toolbar */}
              <div style={{ marginTop: "20px" }}>
                <span style={{ fontSize: "0.82rem", fontWeight: 700, color: "var(--text-muted)", display: "block", marginBottom: "8px" }}>
                  ⚡ 1-Click Action Triggers:
                </span>
                <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                  <Button
                    variant="outline"
                    size="sm"
                    icon={Zap}
                    onClick={() => {
                      setGoalQuery("I want to become a Senior Backend Developer");
                      handleRunAgentWorkflow("I want to become a Senior Backend Developer");
                    }}
                  >
                    🚀 Senior Backend Goal
                  </Button>

                  <Button variant="outline" size="sm" icon={CalendarCheck} onClick={handleExportCalendar}>
                    📅 Export Study Plan (.ics)
                  </Button>

                  <Button variant="outline" size="sm" icon={FileSpreadsheet} onClick={handleExportProgressReport}>
                    📊 Export Progress CSV
                  </Button>
                </div>
              </div>
            </Card>

            {/* Loading Pulse State */}
            {loadingAgent && (
              <Card style={{ textAlign: "center", padding: "44px" }}>
                <div className="typing-indicator" style={{ justifyContent: "center" }}>
                  <span /> <span /> <span />
                </div>
                <p style={{ marginTop: "14px", color: "var(--text-secondary)", fontWeight: 600 }}>
                  Agent Orchestrator coordinating specialized AI agents (Manager → Skill Analyzer → Roadmap Planner)...
                </p>
              </Card>
            )}

            {/* Multi-Agent Output Display */}
            {agentResponse && !loadingAgent && (
              <div>
                <Card style={{ marginBottom: "24px" }}>
                  <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "16px", display: "flex", alignItems: "center", gap: "8px" }}>
                    <Bot size={20} color="var(--color-primary)" /> Multi-Agent Execution Pipeline Network
                  </h3>

                  <div className="pipeline-timeline">
                    {agentResponse.steps.map((step, idx) => (
                      <div key={idx} className="pipeline-step">
                        <div className="pipeline-node">✓</div>
                        <div className="pipeline-label">{step.agent_name.replace(" Agent", "")}</div>
                      </div>
                    ))}
                  </div>

                  <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", marginBottom: "20px" }}>
                    <Badge variant="glow">Confidence: {agentResponse.overall_confidence}%</Badge>
                    <Badge variant="emerald">Latency: {agentResponse.total_execution_time_ms} ms</Badge>
                    <Badge variant="warning">Intent: {agentResponse.workflow_intent}</Badge>
                  </div>

                  <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "16px" }}>
                    🧠 Collaborative Agent Reasoning Steps ({agentResponse.steps.length})
                  </h3>

                  <div style={{ display: "flex", flexDirection: "column" }}>
                    {agentResponse.steps.map((step, idx) => (
                      <AgentReasoningNode key={idx} step={step} stepIndex={idx} />
                    ))}
                  </div>

                  {/* Executive Summary */}
                  <div style={{ marginTop: "24px", background: "var(--bg-surface-elevated)", padding: "24px", borderRadius: "var(--radius-md)", borderLeft: "4px solid var(--color-primary)", border: "1px solid var(--border-color)" }}>
                    <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--color-primary)", marginBottom: "12px", display: "flex", alignItems: "center", gap: "8px" }}>
                      📋 Orchestrator Final Executive Response
                    </h3>
                    <MarkdownRenderer content={agentResponse.final_summary} />
                  </div>

                  {/* Executable Action Box */}
                  {agentResponse.recommended_action && (
                    <div className="executable-action-box">
                      <div>
                        <div style={{ fontWeight: 700, color: "var(--color-success)", fontSize: "0.95rem" }}>
                          ⚡ Recommended Action Ready for Execution
                        </div>
                        <div style={{ fontSize: "0.88rem", color: "var(--text-secondary)", marginTop: "3px" }}>
                          {agentResponse.recommended_action.course_title}
                        </div>
                      </div>

                      <Button variant="glow" onClick={() => handleExecuteRecommendedAction(agentResponse.recommended_action)}>
                        {agentResponse.recommended_action.label}
                      </Button>
                    </div>
                  )}
                </Card>
              </div>
            )}
          </div>
        )}

        {/* Tab 2: Enterprise ChatGPT Interface */}
        {activeTab === "chat" && (
          <div className="chatgpt-layout">
            <Card style={{ display: "flex", flexDirection: "column", padding: 0, overflow: "hidden", border: "1px solid var(--border-color)" }}>
              <div className="chatgpt-header">
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                  <Bot size={22} color="var(--color-primary)" />
                  <div>
                    <span style={{ fontWeight: 700, fontSize: "1rem" }}>Enterprise ChatGPT Session</span>
                    <span style={{ fontSize: "0.78rem", color: "var(--text-muted)", display: "block" }}>Powered by Google Gemini (Model: {systemService.formatModelName(systemInfo.model)})</span>
                  </div>
                </div>

                <Badge variant="glow">Multi-turn Memory Active</Badge>
              </div>

              {/* Chat Messages Stream */}
              <div className="chatgpt-stream">
                {chatMessages.map((msg, idx) => (
                  <div key={idx} className={`chat-bubble ${msg.sender === "user" ? "user-bubble" : "ai-bubble"}`}>
                    <div className="chat-bubble-header">
                      <span>{msg.sender === "user" ? "You" : "Gemini AI Assistant"}</span>
                      <span className="chat-timestamp">{msg.timestamp}</span>
                    </div>
                    {msg.sender === "user" ? (
                      <div>{msg.text}</div>
                    ) : (
                      <MarkdownRenderer content={msg.text} />
                    )}
                  </div>
                ))}

                {loadingChat && (
                  <div className="chat-bubble ai-bubble">
                    <div className="chat-bubble-header">
                      <span>Gemini AI Assistant</span>
                    </div>
                    <div className="typing-indicator">
                      <span /> <span /> <span />
                    </div>
                  </div>
                )}
              </div>

              {/* Suggested Prompts Toolbar */}
              <div className="chat-suggestions">
                {chatSuggestions.map((s, idx) => (
                  <button key={idx} className="suggestion-chip" onClick={() => handleSendDirectChat(s)}>
                    {s}
                  </button>
                ))}
              </div>

              {/* Input Form Bar */}
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSendDirectChat();
                }}
                className="chat-input-bar"
              >
                <input
                  type="text"
                  placeholder="Ask any career development, coding, or enterprise learning question..."
                  value={inputChat}
                  onChange={(e) => setInputChat(e.target.value)}
                />
                <Button type="submit" icon={Send} loading={loadingChat} variant="glow">
                  Send
                </Button>
              </form>
            </Card>
          </div>
        )}
      </div>
    </AppLayout>
  );
}

export default AIAssistant;
