import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import useAuth from "../hooks/useAuth";
import enrollmentService from "../services/enrollmentService";

import "../styles/dashboard.css";

function Dashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [enrollments, setEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchDashboardStats() {
      try {
        const data = await enrollmentService.getMyEnrollments();
        setEnrollments(data);
      } catch (err) {
        console.error("Error loading dashboard enrollments:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchDashboardStats();
  }, []);

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  // Compute Statistics
  const totalEnrolled = enrollments.length;
  const inProgress = enrollments.filter((e) => e.status === "IN_PROGRESS").length;
  const completed = enrollments.filter((e) => e.status === "COMPLETED").length;
  const completionRate =
    totalEnrolled > 0 ? Math.round((completed / totalEnrolled) * 100) : 0;

  // Active / Continue Learning List
  const activeEnrollments = enrollments
    .filter((e) => e.status !== "COMPLETED")
    .slice(0, 3);

  return (
    <div>
      <Navbar />

      <div className="dashboard">
        {/* Welcome Section */}
        <section className="welcome-card">
          <h2>Welcome, {user?.name || "User"} 👋</h2>

          <div className="user-details">
            <p>
              <strong>Email:</strong> {user?.email}
            </p>
            <p>
              <strong>Role:</strong> {user?.role}
            </p>
            <p>
              <strong>Department:</strong> {user?.department || "Engineering"}
            </p>
            <p>
              <strong>Designation:</strong> {user?.designation || "Learner"}
            </p>
          </div>

          <div className="dashboard-actions">
            <button
              className="primary-btn"
              onClick={() => navigate("/my-learning")}
            >
              🎓 Go to My Learning
            </button>
            <button
              className="secondary-btn"
              onClick={() => navigate("/courses")}
            >
              📚 Browse Course Catalog
            </button>
            <button
              className="secondary-btn"
              onClick={() => navigate("/ai")}
            >
              ✨ AI Assistant
            </button>
          </div>
        </section>

        {/* Statistics Widgets */}
        <section className="dashboard-stats-grid">
          <div className="dash-stat-card">
            <div className="dash-stat-icon icon-blue">📘</div>
            <div>
              <div className="dash-stat-value">{totalEnrolled}</div>
              <div className="dash-stat-label">Total Courses Enrolled</div>
            </div>
          </div>

          <div className="dash-stat-card">
            <div className="dash-stat-icon icon-sky">⚡</div>
            <div>
              <div className="dash-stat-value">{inProgress}</div>
              <div className="dash-stat-label">In Progress</div>
            </div>
          </div>

          <div className="dash-stat-card">
            <div className="dash-stat-icon icon-green">🏆</div>
            <div>
              <div className="dash-stat-value">{completed}</div>
              <div className="dash-stat-label">Completed Courses</div>
            </div>
          </div>

          <div className="dash-stat-card">
            <div className="dash-stat-icon icon-purple">📈</div>
            <div>
              <div className="dash-stat-value">{completionRate}%</div>
              <div className="dash-stat-label">Completion Rate</div>
            </div>
          </div>
        </section>

        {/* AI Agent Insights & Risk Forecast Widget */}
        <section className="welcome-card" style={{ background: "linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)", color: "white", marginBottom: "30px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "15px" }}>
            <h3 style={{ fontSize: "1.2rem", fontWeight: 700, display: "flex", alignItems: "center", gap: "8px" }}>
              🤖 AI Agent Insights & Risk Forecast
            </h3>
            <span style={{ fontSize: "0.8rem", background: "rgba(255,255,255,0.15)", padding: "4px 12px", borderRadius: "20px", fontWeight: 700 }}>
              {completionRate >= 50 ? "🟢 LOW DROP-OFF RISK" : (completionRate >= 20 ? "🟡 MEDIUM DROP-OFF RISK" : "🔴 HIGH DROP-OFF RISK")}
            </span>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "15px", fontSize: "0.9rem", color: "#e0e7ff" }}>
            <div style={{ background: "rgba(255,255,255,0.08)", padding: "15px", borderRadius: "10px" }}>
              <div style={{ fontWeight: 700, color: "#a5b4fc", marginBottom: "4px" }}>🎯 Target Role Alignment</div>
              <div>Backend Developer Roadmap (88% Target Readiness)</div>
            </div>

            <div style={{ background: "rgba(255,255,255,0.08)", padding: "15px", borderRadius: "10px" }}>
              <div style={{ fontWeight: 700, color: "#a5b4fc", marginBottom: "4px" }}>📅 Completion Forecast</div>
              <div>Estimated completion in 3 weeks at current velocity</div>
            </div>

            <div style={{ background: "rgba(255,255,255,0.08)", padding: "15px", borderRadius: "10px" }}>
              <div style={{ fontWeight: 700, color: "#a5b4fc", marginBottom: "4px" }}>⚡ Weekly AI Recommendation</div>
              <div>Complete 2 lessons per week to maintain optimal momentum</div>
            </div>
          </div>
        </section>

        {/* Today's Learning Plan & Tasks */}
        <section className="welcome-card" style={{ marginBottom: "30px" }}>
          <h3 style={{ fontSize: "1.15rem", fontWeight: 700, color: "#0f172a", marginBottom: "15px", display: "flex", alignItems: "center", gap: "8px" }}>
            📅 Today's AI Suggested Learning Plan & Tasks
          </h3>

          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "#f8fafc", padding: "12px 16px", borderRadius: "8px", borderLeft: "4px solid #3b82f6" }}>
              <div>
                <span style={{ fontWeight: 700, color: "#1e293b" }}>Task 1: Complete Module 2 Video Lessons</span>
                <div style={{ fontSize: "0.82rem", color: "#64748b", marginTop: "2px" }}>Est. 45 mins • Course: Python & FastAPI Architecture</div>
              </div>
              <span style={{ fontSize: "0.75rem", background: "#dbeafe", color: "#1e40af", padding: "2px 8px", borderRadius: "10px", fontWeight: 700 }}>HIGH PRIORITY</span>
            </div>

            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "#f8fafc", padding: "12px 16px", borderRadius: "8px", borderLeft: "4px solid #10b981" }}>
              <div>
                <span style={{ fontWeight: 700, color: "#1e293b" }}>Task 2: Practice PostgreSQL Relational Queries</span>
                <div style={{ fontSize: "0.82rem", color: "#64748b", marginTop: "2px" }}>Est. 30 mins • Lab: Database Migrations</div>
              </div>
              <span style={{ fontSize: "0.75rem", background: "#d1fae5", color: "#065f46", padding: "2px 8px", borderRadius: "10px", fontWeight: 700 }}>RECOMMENDED</span>
            </div>
          </div>
        </section>

        {/* Continue Learning Quick Access */}
        <section className="continue-learning-section">
          <h3 style={{ fontSize: "1.2rem", fontWeight: 700, color: "#1e293b" }}>
            ▶️ Continue Learning
          </h3>

          {loading ? (
            <p style={{ marginTop: "10px", color: "#64748b" }}>Loading learning stats...</p>
          ) : activeEnrollments.length === 0 ? (
            <p style={{ marginTop: "10px", color: "#64748b" }}>
              No active courses in progress. Explore courses or generate an AI path!
            </p>
          ) : (
            <div className="continue-grid">
              {activeEnrollments.map((item) => {
                const course = item.course || {};
                const progress = item.progress_percentage || 0;

                return (
                  <div key={item.id} className="continue-card">
                    <div>
                      <div className="continue-card-title">
                        {course.title || "Course"}
                      </div>
                      <span
                        style={{
                          fontSize: "0.78rem",
                          background: "#e2e8f0",
                          padding: "2px 8px",
                          borderRadius: "10px",
                          fontWeight: 600,
                        }}
                      >
                        {course.category || "General"}
                      </span>
                    </div>

                    <div style={{ marginTop: "15px" }}>
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          fontSize: "0.8rem",
                          marginBottom: "4px",
                          fontWeight: 600,
                        }}
                      >
                        <span>Progress</span>
                        <span>{progress}%</span>
                      </div>

                      <div
                        style={{
                          height: "8px",
                          background: "#cbd5e1",
                          borderRadius: "6px",
                          overflow: "hidden",
                          marginBottom: "12px",
                        }}
                      >
                        <div
                          style={{
                            height: "100%",
                            width: `${progress}%`,
                            background: "#2563eb",
                            borderRadius: "6px",
                            transition: "width 0.3s ease",
                          }}
                        ></div>
                      </div>

                      <button
                        className="primary-btn"
                        style={{ width: "100%", padding: "8px", fontSize: "0.85rem" }}
                        onClick={() => navigate("/my-learning")}
                      >
                        Resume Course
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

export default Dashboard;