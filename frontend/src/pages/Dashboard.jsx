import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  BookOpen,
  Award,
  ShieldCheck,
  Flame,
  TrendingUp,
  Zap,
  PlayCircle,
  Calendar,
  Sparkles,
  AlertTriangle,
  ArrowRight,
} from "lucide-react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

import AppLayout from "../components/AppLayout";
import StatCard from "../components/common/StatCard";
import ChartCard from "../components/common/ChartCard";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Badge from "../components/common/Badge";
import useAuth from "../hooks/useAuth";
import enrollmentService from "../services/enrollmentService";
import "../styles/dashboard.css";

const velocityData = [
  { day: "Mon", hours: 1.5 },
  { day: "Tue", hours: 2.0 },
  { day: "Wed", hours: 1.8 },
  { day: "Thu", hours: 3.2 },
  { day: "Fri", hours: 2.5 },
  { day: "Sat", hours: 4.0 },
  { day: "Sun", hours: 3.5 },
];

const skillDistributionData = [
  { name: "Python & Backend", value: 40, color: "#6366f1" },
  { name: "PostgreSQL Data", value: 30, color: "#8b5cf6" },
  { name: "FastAPI REST", value: 20, color: "#22c55e" },
  { name: "Cloud & DevOps", value: 10, color: "#f59e0b" },
];

function Dashboard() {
  const navigate = useNavigate();
  const { user } = useAuth();
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

  const totalEnrolled = enrollments.length;
  const inProgress = enrollments.filter((e) => e.status === "IN_PROGRESS").length;
  const completed = enrollments.filter((e) => e.status === "COMPLETED").length;
  const certificatesCount = enrollments.filter((e) => e.certificate_generated).length;
  const completionRate =
    totalEnrolled > 0 ? Math.round((completed / totalEnrolled) * 100) : 0;

  const activeEnrollments = enrollments
    .filter((e) => e.status !== "COMPLETED")
    .slice(0, 3);

  return (
    <AppLayout>
      <div className="dash-container">
        {/* Welcome Banner */}
        <div className="dash-welcome-banner">
          <div>
            <span className="dash-welcome-tag">Enterprise Learner Workspace</span>
            <h1>Welcome back, {user?.name || "Learner"} 👋</h1>
            <p>
              Target Role: <strong>{user?.designation || "Backend Engineer"}</strong> ({user?.department || "Engineering"})
            </p>
          </div>

          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
            <Button icon={Sparkles} onClick={() => navigate("/ai")}>
              Ask AI Agent
            </Button>
            <Button variant="outline" icon={BookOpen} onClick={() => navigate("/courses")}>
              Explore Courses
            </Button>
          </div>
        </div>

        {/* 6 SaaS KPI StatCards */}
        <div className="dash-kpi-grid">
          <StatCard
            title="Courses Enrolled"
            value={totalEnrolled}
            icon={BookOpen}
            color="indigo"
            description="Active catalog enrollments"
          />
          <StatCard
            title="In Progress"
            value={inProgress}
            icon={Zap}
            color="purple"
            description="Active study modules"
          />
          <StatCard
            title="Courses Completed"
            value={completed}
            icon={Award}
            color="emerald"
            description="100% finished modules"
          />
          <StatCard
            title="Digital Certificates"
            value={certificatesCount}
            icon={ShieldCheck}
            color="indigo"
            description="Issued credentials"
          />
          <StatCard
            title="Learning Streak"
            value="7 Days 🔥"
            icon={Flame}
            color="amber"
            description="Consistent daily learning"
          />
          <StatCard
            title="Avg Completion Rate"
            value={`${completionRate}%`}
            icon={TrendingUp}
            color="emerald"
            description="Target role velocity"
          />
        </div>

        {/* Recharts Analytics Section */}
        <div className="dash-charts-grid">
          <ChartCard title="📈 Learning Velocity Trend" subtitle="Hours spent per day this week">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={velocityData}>
                <defs>
                  <linearGradient id="velocityGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="day" stroke="var(--text-muted)" fontSize={12} />
                <YAxis stroke="var(--text-muted)" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    background: "var(--bg-surface)",
                    borderColor: "var(--border-color)",
                    borderRadius: "8px",
                  }}
                />
                <Area type="monotone" dataKey="hours" stroke="#6366f1" strokeWidth={3} fillOpacity={1} fill="url(#velocityGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </ChartCard>

          <ChartCard title="📊 Skill Distribution" subtitle="Technical competency allocation">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={skillDistributionData} cx="50%" cy="50%" innerRadius={55} outerRadius={85} paddingAngle={4} dataKey="value">
                  {skillDistributionData.map((entry, idx) => (
                    <Cell key={idx} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    background: "var(--bg-surface)",
                    borderColor: "var(--border-color)",
                    borderRadius: "8px",
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* AI Risk Forecast & Today's Tasks */}
        <div className="dash-two-col">
          <Card style={{ background: "linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)", color: "white" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
              <h3 style={{ fontSize: "1.15rem", fontWeight: 700, color: "white", display: "flex", alignItems: "center", gap: "8px" }}>
                <Sparkles size={20} color="#a5b4fc" /> AI Drop-Off Risk & Insights
              </h3>
              <Badge variant={completionRate >= 50 ? "success" : "warning"}>
                {completionRate >= 50 ? "🟢 LOW RISK" : "🟡 MEDIUM RISK"}
              </Badge>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "12px", fontSize: "0.9rem", color: "#cbd5e1" }}>
              <div style={{ background: "rgba(255,255,255,0.06)", padding: "12px", borderRadius: "10px" }}>
                <strong style={{ color: "#a5b4fc" }}>Target Role Alignment:</strong> Senior Backend Engineer Roadmap (88% Readiness)
              </div>
              <div style={{ background: "rgba(255,255,255,0.06)", padding: "12px", borderRadius: "10px" }}>
                <strong style={{ color: "#a5b4fc" }}>Completion Forecast:</strong> On track to finish in 3 weeks at 2.5 hrs/day
              </div>
            </div>
          </Card>

          <Card>
            <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "16px", display: "flex", alignItems: "center", gap: "8px" }}>
              <Calendar size={20} color="var(--color-primary)" /> Today's Suggested Learning Tasks
            </h3>

            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px", background: "var(--bg-primary)", borderRadius: "var(--radius-md)" }}>
                <div>
                  <div style={{ fontWeight: 700, fontSize: "0.9rem" }}>Task 1: Complete FastAPI Async Endpoints Lab</div>
                  <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>45 mins • Course: Python & FastAPI</div>
                </div>
                <Badge variant="primary">HIGH PRIORITY</Badge>
              </div>

              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px", background: "var(--bg-primary)", borderRadius: "var(--radius-md)" }}>
                <div>
                  <div style={{ fontWeight: 700, fontSize: "0.9rem" }}>Task 2: Review PostgreSQL Indexing & Query Tuning</div>
                  <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>30 mins • Lab: Database Migrations</div>
                </div>
                <Badge variant="purple">RECOMMENDED</Badge>
              </div>
            </div>
          </Card>
        </div>

        {/* Continue Learning Grid */}
        <div style={{ marginTop: "28px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
            <h2 style={{ fontSize: "1.25rem", fontWeight: 700 }}>▶️ Continue Learning</h2>
            <Button variant="ghost" onClick={() => navigate("/my-learning")}>
              View All <ArrowRight size={16} />
            </Button>
          </div>

          {activeEnrollments.length === 0 ? (
            <Card style={{ textAlign: "center", padding: "32px" }}>
              <p style={{ color: "var(--text-muted)" }}>No active course progress. Browse courses to get started!</p>
            </Card>
          ) : (
            <div className="dash-continue-grid">
              {activeEnrollments.map((item) => {
                const course = item.course || {};
                const progress = item.progress_percentage || 0;

                return (
                  <Card key={item.id}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
                      <h4 style={{ fontSize: "1rem", fontWeight: 700 }}>{course.title || "Course"}</h4>
                      <Badge variant="purple">{course.category || "General"}</Badge>
                    </div>

                    <div style={{ marginTop: "16px" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.82rem", fontWeight: 600, marginBottom: "6px" }}>
                        <span>Progress</span>
                        <span>{progress}%</span>
                      </div>

                      <div style={{ height: "8px", background: "var(--border-color)", borderRadius: "var(--radius-full)", overflow: "hidden", marginBottom: "16px" }}>
                        <div style={{ height: "100%", width: `${progress}%`, background: "var(--color-primary)", borderRadius: "var(--radius-full)" }} />
                      </div>

                      <Button icon={PlayCircle} style={{ width: "100%" }} onClick={() => navigate("/my-learning")}>
                        Resume Course
                      </Button>
                    </div>
                  </Card>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
}

export default Dashboard;