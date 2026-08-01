import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
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
  ArrowRight,
  Target,
  CheckCircle2,
  Clock,
  Compass,
  FileCheck,
  Activity,
  ChevronRight,
} from "lucide-react";
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  LineChart,
  Line,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import AppLayout from "../components/AppLayout";
import MetricCard from "../components/common/MetricCard";
import ChartCard from "../components/common/ChartCard";
import SectionHeader from "../components/common/SectionHeader";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Badge from "../components/common/Badge";
import ProgressRing from "../components/common/ProgressRing";
import useAuth from "../hooks/useAuth";
import enrollmentService from "../services/enrollmentService";
import systemService from "../services/systemService";
import "../styles/dashboard.css";

const weeklyProgressData = [
  { day: "Mon", lessons: 2 },
  { day: "Tue", lessons: 4 },
  { day: "Wed", lessons: 3 },
  { day: "Thu", lessons: 6 },
  { day: "Fri", lessons: 5 },
  { day: "Sat", lessons: 8 },
  { day: "Sun", lessons: 7 },
];

const studyHoursData = [
  { day: "Mon", hours: 1.5 },
  { day: "Tue", hours: 2.0 },
  { day: "Wed", hours: 1.8 },
  { day: "Thu", hours: 3.2 },
  { day: "Fri", hours: 2.5 },
  { day: "Sat", hours: 4.0 },
  { day: "Sun", hours: 3.5 },
];

const skillRadarData = [
  { subject: "Python Async", A: 120, fullMark: 150 },
  { subject: "FastAPI REST", A: 140, fullMark: 150 },
  { subject: "PostgreSQL DB", A: 110, fullMark: 150 },
  { subject: "ChromaDB RAG", A: 130, fullMark: 150 },
  { subject: "Multi-Agent AI", A: 145, fullMark: 150 },
  { subject: "System Design", A: 100, fullMark: 150 },
];

const learningVelocityData = [
  { week: "Wk 1", velocity: 65 },
  { week: "Wk 2", velocity: 72 },
  { week: "Wk 3", velocity: 84 },
  { week: "Wk 4", velocity: 96 },
];

function Dashboard() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [enrollments, setEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [systemInfo, setSystemInfo] = useState({
    provider: "AI Provider",
    model: "Active Model",
    status: "Operational",
  });


  useEffect(() => {
    systemService.getSystemInfo().then(setSystemInfo).catch(() => {});
  }, []);

  useEffect(() => {
    async function fetchDashboardStats() {
      try {
        const data = await enrollmentService.getMyEnrollments();
        setEnrollments(data || []);
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
      <div className="dash-workspace">
        {/* Productivity Workspace Hero */}
        <motion.div
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="workspace-hero-card"
        >
          <div className="hero-left-col">
            <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "10px" }}>
              <Badge variant="glow" icon={Sparkles}>
                Enterprise AI Command Center
              </Badge>
              <span className="text-caption" style={{ color: "var(--color-success)", fontWeight: 700 }}>
                🟢 Session Verified
              </span>
            </div>

            <h1 className="text-hero">Welcome back, {user?.name || "Learner"} 👋</h1>
            <p className="text-body" style={{ color: "var(--text-secondary)", marginTop: "6px" }}>
              Role: <strong style={{ color: "var(--text-primary)" }}>{user?.designation || "Senior Engineer"}</strong> ({user?.department || "Engineering"}) • {systemInfo.provider} ({systemService.formatModelName(systemInfo.model)}) Active
            </p>

            <div className="hero-metrics-strip">
              <div className="hero-metric-item">
                <span className="text-caption">Current Pathway</span>
                <strong style={{ color: "var(--color-primary)", display: "flex", alignItems: "center", gap: "4px" }}>
                  <Target size={14} /> Senior Backend Architect
                </strong>
              </div>

              <div className="hero-metric-item">
                <span className="text-caption">Target Role Readiness</span>
                <strong style={{ color: "var(--color-success)" }}>88% Match Index</strong>
              </div>

              <div className="hero-metric-item">
                <span className="text-caption">AI Confidence Index</span>
                <strong style={{ color: "var(--color-secondary)" }}>96% High Accuracy</strong>
              </div>
            </div>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: "24px" }}>
            {/* SVG Progress Ring */}
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "6px" }}>
              <ProgressRing progress={88} size={90} strokeWidth={8} color="var(--color-primary)" label="Readiness" />
            </div>

            <div className="hero-actions-col">
              <Button icon={Sparkles} variant="glow" onClick={() => navigate("/ai")}>
                Ask AI Assistant
              </Button>
              <Button variant="outline" icon={PlayCircle} onClick={() => navigate("/my-learning")}>
                Continue Learning
              </Button>
              <Button variant="ghost" icon={Compass} onClick={() => navigate("/courses")}>
                Explore Catalog
              </Button>
              <Button variant="ghost" icon={FileCheck} onClick={() => navigate("/my-learning")}>
                My Certificates
              </Button>
            </div>
          </div>
        </motion.div>

        {/* 6 Responsive KPI Metric Cards */}
        <div className="dash-metrics-grid">
          <MetricCard
            title="Courses Enrolled"
            value={totalEnrolled}
            icon={BookOpen}
            trend="+12% this month"
            color="indigo"
            description="Active course catalog"
          />
          <MetricCard
            title="In Progress"
            value={inProgress}
            icon={Zap}
            trend="Active learning"
            color="purple"
            description="Current study modules"
          />
          <MetricCard
            title="Courses Completed"
            value={completed}
            icon={Award}
            trend="+2 this week"
            color="emerald"
            description="100% finished courses"
          />
          <MetricCard
            title="Digital Credentials"
            value={certificatesCount}
            icon={ShieldCheck}
            trend="100% Verified"
            color="indigo"
            description="Issued certificates"
          />
          <MetricCard
            title="Learning Streak"
            value="7 Days 🔥"
            icon={Flame}
            trend="Personal Best"
            color="amber"
            description="Consistent study daily"
          />
          <MetricCard
            title="Avg Progress"
            value={`${completionRate}%`}
            icon={TrendingUp}
            trend="+15.4% velocity"
            color="emerald"
            description="Target role velocity"
          />
        </div>

        {/* Recharts Analytics Grid 1: Weekly Progress & Skill Radar */}
        <div className="dash-charts-2col" style={{ marginTop: "28px" }}>
          <ChartCard title="📈 Weekly Learning Progress" subtitle="Modules completed per day">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={weeklyProgressData}>
                <defs>
                  <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--color-primary)" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="var(--color-primary)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="day" stroke="var(--text-muted)" fontSize={12} />
                <YAxis stroke="var(--text-muted)" fontSize={12} />
                <Tooltip contentStyle={{ background: "var(--bg-surface)", borderColor: "var(--border-color)", borderRadius: "12px", color: "var(--text-primary)" }} />
                <Area type="monotone" dataKey="lessons" stroke="var(--color-primary)" strokeWidth={3} fillOpacity={1} fill="url(#areaGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </ChartCard>

          <ChartCard title="🎯 Technical Skill Competency Radar" subtitle="Multi-domain competency assessment">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={skillRadarData}>
                <PolarGrid stroke="var(--border-color)" />
                <PolarAngleAxis dataKey="subject" stroke="var(--text-muted)" fontSize={11} />
                <Radar name="Competency" dataKey="A" stroke="var(--color-primary)" fill="var(--color-primary)" fillOpacity={0.3} />
              </RadarChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Recharts Analytics Grid 2: Daily Study Hours & Learning Velocity */}
        <div className="dash-charts-2col" style={{ marginTop: "24px" }}>
          <ChartCard title="📊 Daily Study Hours" subtitle="Hours invested this week">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={studyHoursData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="day" stroke="var(--text-muted)" fontSize={12} />
                <YAxis stroke="var(--text-muted)" fontSize={12} />
                <Tooltip contentStyle={{ background: "var(--bg-surface)", borderColor: "var(--border-color)", borderRadius: "12px", color: "var(--text-primary)" }} />
                <Bar dataKey="hours" fill="var(--color-secondary)" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>

          <ChartCard title="🚀 Learning Velocity Trajectory" subtitle="Target role readiness velocity">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={learningVelocityData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="week" stroke="var(--text-muted)" fontSize={12} />
                <YAxis stroke="var(--text-muted)" fontSize={12} />
                <Tooltip contentStyle={{ background: "var(--bg-surface)", borderColor: "var(--border-color)", borderRadius: "12px", color: "var(--text-primary)" }} />
                <Line type="monotone" dataKey="velocity" stroke="var(--color-success)" strokeWidth={3} dot={{ r: 5 }} />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* AI Drop-Off Risk & Today's Tasks */}
        <div className="dash-charts-2col" style={{ marginTop: "24px" }}>
          <Card variant="hero">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
              <h3 style={{ fontSize: "1.1rem", fontWeight: 700, display: "flex", alignItems: "center", gap: "8px" }}>
                <Sparkles size={20} color="var(--color-primary)" /> AI Drop-Off Risk Forecast
              </h3>
              <Badge variant={completionRate >= 50 ? "success" : "warning"}>
                {completionRate >= 50 ? "LOW RISK" : "MEDIUM RISK"}
              </Badge>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "12px", fontSize: "14px" }}>
              <div style={{ background: "var(--bg-surface)", padding: "14px 16px", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-color)" }}>
                <strong style={{ color: "var(--color-primary)" }}>Target Role Alignment:</strong> Senior Backend Architect (88% Readiness Score)
              </div>
              <div style={{ background: "var(--bg-surface)", padding: "14px 16px", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-color)" }}>
                <strong style={{ color: "var(--color-primary)" }}>Completion Forecast:</strong> On track to achieve certification in 3 weeks at 2.5 hrs/day
              </div>
            </div>
          </Card>

          <Card>
            <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "16px", display: "flex", alignItems: "center", gap: "8px" }}>
              <Calendar size={20} color="var(--color-primary)" /> Today's Suggested Learning Tasks
            </h3>

            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 16px", background: "var(--bg-surface-elevated)", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-color)" }}>
                <div>
                  <div style={{ fontWeight: 700, fontSize: "14px" }}>Task 1: Complete FastAPI Async Endpoints Lab</div>
                  <div className="text-caption">45 mins • Course: Python & FastAPI</div>
                </div>
                <Badge variant="glow">HIGH PRIORITY</Badge>
              </div>

              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 16px", background: "var(--bg-surface-elevated)", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-color)" }}>
                <div>
                  <div style={{ fontWeight: 700, fontSize: "14px" }}>Task 2: Review PostgreSQL Indexing & Tuning</div>
                  <div className="text-caption">30 mins • Lab: Database Migrations</div>
                </div>
                <Badge variant="outline">RECOMMENDED</Badge>
              </div>
            </div>
          </Card>
        </div>

        {/* Continue Learning Grid */}
        <div style={{ marginTop: "36px" }}>
          <SectionHeader
            title="Continue Learning"
            subtitle="Resume active module paths where you left off"
            action={
              <Button variant="ghost" onClick={() => navigate("/my-learning")}>
                View All <ArrowRight size={16} />
              </Button>
            }
          />

          {activeEnrollments.length === 0 ? (
            <Card style={{ textAlign: "center", padding: "40px" }}>
              <p style={{ color: "var(--text-muted)" }}>No active course progress. Browse catalog to start learning!</p>
              <Button style={{ marginTop: "14px" }} onClick={() => navigate("/courses")}>
                Browse Catalog
              </Button>
            </Card>
          ) : (
            <div className="dash-continue-grid">
              {activeEnrollments.map((item) => {
                const course = item.course || {};
                const progress = item.progress_percentage || 0;

                return (
                  <Card key={item.id} hoverEffect style={{ display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
                    <div>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
                        <h4 className="text-card-title">{course.title || "Course"}</h4>
                        <Badge variant="indigo">{course.category || "General"}</Badge>
                      </div>
                      <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "16px" }}>
                        {course.description}
                      </p>
                    </div>

                    <div style={{ marginTop: "auto" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "13px", fontWeight: 600, marginBottom: "6px" }}>
                        <span>Progress</span>
                        <span>{progress}%</span>
                      </div>

                      <div style={{ height: "8px", background: "var(--border-color)", borderRadius: "var(--radius-full)", overflow: "hidden", marginBottom: "16px" }}>
                        <div style={{ height: "100%", width: `${progress}%`, background: "var(--gradient-cta)", borderRadius: "var(--radius-full)" }} />
                      </div>

                      <Button icon={PlayCircle} style={{ width: "100%" }} onClick={() => navigate("/my-learning")}>
                        Resume Module
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