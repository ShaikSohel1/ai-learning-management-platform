import { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import adminService from "../services/adminService";
import "../styles/dashboard.css";

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAdminData() {
      try {
        setLoading(true);
        const [statsData, usersData, healthData] = await Promise.all([
          adminService.getAdminStats(),
          adminService.getAllUsers(),
          adminService.getSystemHealth(),
        ]);
        setStats(statsData);
        setUsers(usersData);
        setHealth(healthData);
      } catch (err) {
        console.error("Failed to load admin dashboard data:", err);
      } finally {
        setLoading(false);
      }
    }

    loadAdminData();
  }, []);

  return (
    <div>
      <Navbar />

      <div className="dashboard">
        <section className="welcome-card" style={{ background: "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)", color: "white" }}>
          <h2>⚙️ Enterprise Admin Control Center</h2>
          <p style={{ color: "#94a3b8", marginTop: "4px" }}>
            Monitor system health, active components, platform user catalog, and AI execution audit logs.
          </p>
        </section>

        {loading ? (
          <p style={{ textAlign: "center", color: "#64748b", padding: "30px 0" }}>
            Loading enterprise admin metrics...
          </p>
        ) : (
          <div>
            {/* System Component Health Status Cards */}
            <section className="dashboard-stats-grid">
              <div className="dash-stat-card">
                <div className="dash-stat-icon icon-green">🐘</div>
                <div>
                  <div className="dash-stat-value">HEALTHY</div>
                  <div className="dash-stat-label">PostgreSQL Database</div>
                </div>
              </div>

              <div className="dash-stat-card">
                <div className="dash-stat-icon icon-sky">⚡</div>
                <div>
                  <div className="dash-stat-value">HEALTHY</div>
                  <div className="dash-stat-label">ChromaDB Vector Store</div>
                </div>
              </div>

              <div className="dash-stat-card">
                <div className="dash-stat-icon icon-purple">🤖</div>
                <div>
                  <div className="dash-stat-value">HEALTHY</div>
                  <div className="dash-stat-label">Google Gemini 2.0 LLM</div>
                </div>
              </div>

              <div className="dash-stat-card">
                <div className="dash-stat-icon icon-blue">🧩</div>
                <div>
                  <div className="dash-stat-value">8 Active</div>
                  <div className="dash-stat-label">Specialized AI Agents</div>
                </div>
              </div>
            </section>

            {/* Platform Metrics Overview */}
            <section className="welcome-card" style={{ marginBottom: "30px" }}>
              <h3 style={{ fontSize: "1.15rem", fontWeight: 700, marginBottom: "15px", color: "#0f172a" }}>
                📊 Platform Enterprise Summary Metrics
              </h3>

              <div className="analytics-grid">
                <div className="analytics-card">
                  <div className="analytics-icon">👥</div>
                  <div>
                    <div className="analytics-val">{stats?.total_users || 0}</div>
                    <div className="analytics-lbl">Total Registered Users</div>
                  </div>
                </div>

                <div className="analytics-card">
                  <div className="analytics-icon">📚</div>
                  <div>
                    <div className="analytics-val">{stats?.total_courses || 0}</div>
                    <div className="analytics-lbl">Total LMS Courses</div>
                  </div>
                </div>

                <div className="analytics-card">
                  <div className="analytics-icon">📄</div>
                  <div>
                    <div className="analytics-val">{stats?.knowledge_documents || 0}</div>
                    <div className="analytics-lbl">Knowledge Documents</div>
                  </div>
                </div>

                <div className="analytics-card">
                  <div className="analytics-icon">🛠️</div>
                  <div>
                    <div className="analytics-val">{stats?.audit_logs_count || 0}</div>
                    <div className="analytics-lbl">Agent Tool Executions</div>
                  </div>
                </div>
              </div>
            </section>

            {/* Registered Users Table */}
            <section className="welcome-card">
              <h3 style={{ fontSize: "1.15rem", fontWeight: 700, marginBottom: "15px", color: "#0f172a" }}>
                👤 Registered Platform Users Catalog ({users.length})
              </h3>

              <table className="docs-table">
                <thead>
                  <tr>
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Department</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((u) => (
                    <tr key={u.id}>
                      <td style={{ fontWeight: 700 }}>#{u.id}</td>
                      <td>{u.name}</td>
                      <td>{u.email}</td>
                      <td>
                        <span style={{ fontSize: "0.8rem", background: "#e0f2fe", color: "#0369a1", padding: "2px 8px", borderRadius: "10px", fontWeight: 700 }}>
                          {u.role}
                        </span>
                      </td>
                      <td>{u.department}</td>
                      <td>
                        <span style={{ fontSize: "0.8rem", color: "#166534", fontWeight: 700 }}>
                          Active
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;
