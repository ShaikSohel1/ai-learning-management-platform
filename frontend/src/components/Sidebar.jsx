import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  BookOpen,
  GraduationCap,
  Sparkles,
  Database,
  Settings,
  LogOut,
  ChevronLeft,
  ChevronRight,
  BrainCircuit,
  Zap,
} from "lucide-react";

import useAuth from "../hooks/useAuth";
import "../styles/sidebar.css";

export function Sidebar({ collapsed, setCollapsed }) {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout, user } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const navItems = [
    { label: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
    { label: "Courses Catalog", path: "/courses", icon: BookOpen },
    { label: "My Learning", path: "/my-learning", icon: GraduationCap },
    { label: "AI Assistant", path: "/ai", icon: Sparkles, badge: "AI" },
    { label: "Knowledge Base", path: "/knowledge", icon: Database },
    { label: "Admin Console", path: "/admin", icon: Settings },
  ];

  return (
    <aside className={`app-sidebar ${collapsed ? "collapsed" : ""}`}>
      {/* Top Header Logo */}
      <div className="sidebar-header">
        <Link to="/dashboard" className="sidebar-logo">
          <div className="sidebar-logo-badge">
            <BrainCircuit size={20} />
          </div>
          {!collapsed && (
            <div style={{ display: "flex", flexDirection: "column" }}>
              <span style={{ fontSize: "1rem", lineHeight: 1.2 }}>AI LMS</span>
              <span style={{ fontSize: "0.68rem", color: "var(--text-muted)", fontWeight: 600 }}>ENTERPRISE</span>
            </div>
          )}
        </Link>

        <button
          className="sidebar-toggle-btn"
          onClick={() => setCollapsed(!collapsed)}
          title={collapsed ? "Expand Sidebar" : "Collapse Sidebar"}
        >
          {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
      </div>

      {/* Navigation Links */}
      {!collapsed && <div className="sidebar-section-title">Navigation</div>}
      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`sidebar-link ${isActive ? "active" : ""}`}
              title={collapsed ? item.label : ""}
            >
              <Icon size={19} />
              {!collapsed && (
                <div style={{ flex: 1, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span>{item.label}</span>
                  {item.badge && (
                    <span
                      style={{
                        fontSize: "0.65rem",
                        padding: "2px 6px",
                        borderRadius: "8px",
                        background: "var(--color-primary-light)",
                        color: "var(--color-primary)",
                        fontWeight: 800,
                      }}
                    >
                      {item.badge}
                    </span>
                  )}
                </div>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Footer / User Profile & Logout */}
      <div className="sidebar-footer">
        {!collapsed && user && (
          <div
            style={{
              padding: "8px 10px",
              background: "var(--bg-surface)",
              borderRadius: "var(--radius-sm)",
              border: "1px solid var(--border-color)",
              marginBottom: "8px",
              display: "flex",
              alignItems: "center",
              gap: "10px",
            }}
          >
            <div
              style={{
                width: "32px",
                height: "32px",
                borderRadius: "50%",
                background: "var(--gradient-cta)",
                color: "white",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontWeight: 700,
                fontSize: "0.85rem",
              }}
            >
              {user.name ? user.name[0].toUpperCase() : "U"}
            </div>
            <div style={{ overflow: "hidden" }}>
              <div style={{ fontSize: "0.82rem", fontWeight: 700, whiteSpace: "nowrap", textOverflow: "ellipsis", overflow: "hidden" }}>
                {user.name || "User"}
              </div>
              <div style={{ fontSize: "0.72rem", color: "var(--text-muted)", whiteSpace: "nowrap", textOverflow: "ellipsis", overflow: "hidden" }}>
                {user.role || "Student"}
              </div>
            </div>
          </div>
        )}

        <button
          onClick={handleLogout}
          className="sidebar-link"
          style={{ background: "transparent", border: "none", width: "100%", cursor: "pointer" }}
          title={collapsed ? "Logout" : ""}
        >
          <LogOut size={19} color="var(--color-danger)" />
          {!collapsed && <span style={{ color: "var(--color-danger)" }}>Logout</span>}
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;
