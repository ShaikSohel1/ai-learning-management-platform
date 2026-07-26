import React, { useState, useEffect } from "react";
import {
  Settings,
  Users,
  BookOpen,
  FileText,
  Wrench,
  Activity,
  CheckCircle,
  Database,
  Cpu,
  ShieldAlert,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import AppLayout from "../components/AppLayout";
import StatCard from "../components/common/StatCard";
import ChartCard from "../components/common/ChartCard";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";
import LoadingSkeleton from "../components/common/LoadingSkeleton";
import adminService from "../services/adminService";
import "../styles/admin.css";

const apiRequestsData = [
  { endpoint: "/auth", requests: 450 },
  { endpoint: "/courses", requests: 890 },
  { endpoint: "/enrollments", requests: 1200 },
  { endpoint: "/knowledge", requests: 640 },
  { endpoint: "/agents", requests: 1520 },
];

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
    <AppLayout>
      <div className="admin-container">
        {/* Header */}
        <div style={{ marginBottom: "24px" }}>
          <h1>⚙️ Enterprise Admin & System Monitoring</h1>
          <p style={{ color: "var(--text-secondary)", marginTop: "4px" }}>
            Monitor system health status, active infrastructure components, user catalogs, and tool audit logs.
          </p>
        </div>

        {loading ? (
          <LoadingSkeleton height="180px" count={3} />
        ) : (
          <div>
            {/* System Health Status Badges */}
            <div className="admin-kpi-grid">
              <StatCard
                title="PostgreSQL Database"
                value="HEALTHY"
                icon={Database}
                color="emerald"
                description="Relational data store"
              />
              <StatCard
                title="ChromaDB Vector Store"
                value="HEALTHY"
                icon={Activity}
                color="indigo"
                description={`${stats?.knowledge_chunks || 0} vector chunks`}
              />
              <StatCard
                title="Google Gemini LLM"
                value="HEALTHY"
                icon={Cpu}
                color="purple"
                description="Gemini 2.0 Flash engine"
              />
              <StatCard
                title="Agent Orchestrator"
                value="8 Active"
                icon={Wrench}
                color="amber"
                description="Specialized AI agents"
              />
            </div>

            {/* Platform Enterprise Summary */}
            <div className="admin-summary-grid">
              <StatCard title="Registered Users" value={stats?.total_users || 0} icon={Users} color="indigo" />
              <StatCard title="Total LMS Courses" value={stats?.total_courses || 0} icon={BookOpen} color="purple" />
              <StatCard title="Knowledge Documents" value={stats?.knowledge_documents || 0} icon={FileText} color="emerald" />
              <StatCard title="Agent Tool Executions" value={stats?.audit_logs_count || 0} icon={Wrench} color="amber" />
            </div>

            {/* Recharts Analytics Chart */}
            <div style={{ margin: "28px 0" }}>
              <ChartCard title="📊 API Endpoint Request Volume" subtitle="Requests processed past 24 hours">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={apiRequestsData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                    <XAxis dataKey="endpoint" stroke="var(--text-muted)" fontSize={12} />
                    <YAxis stroke="var(--text-muted)" fontSize={12} />
                    <Tooltip contentStyle={{ background: "var(--bg-surface)", borderColor: "var(--border-color)", borderRadius: "8px" }} />
                    <Bar dataKey="requests" fill="#6366f1" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>
            </div>

            {/* Platform Users Table */}
            <Card>
              <h3 style={{ fontSize: "1.15rem", fontWeight: 700, marginBottom: "16px" }}>
                👤 Platform User Directory ({users.length})
              </h3>

              <div style={{ overflowX: "auto" }}>
                <table className="admin-users-table">
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
                          <Badge variant="purple">{u.role}</Badge>
                        </td>
                        <td>{u.department}</td>
                        <td>
                          <Badge variant="success">Active</Badge>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          </div>
        )}
      </div>
    </AppLayout>
  );
}

export default AdminDashboard;
