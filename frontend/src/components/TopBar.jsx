import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Search, Bell, Check, X, Command, Activity, Sparkles, User } from "lucide-react";
import useAuth from "../hooks/useAuth";
import notificationService from "../services/notificationService";
import systemService from "../services/systemService";
import CommandPalette from "./CommandPalette";
import ProfileModal from "./ProfileModal";
import "../styles/topBar.css";

export function TopBar({ collapsed }) {
  const location = useLocation();
  const { user } = useAuth();

  const [notifications, setNotifications] = useState([]);
  const [showDrawer, setShowDrawer] = useState(false);
  const [cmdOpen, setCmdOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [systemInfo, setSystemInfo] = useState({
    provider: "Google Gemini",
    model: "models/gemini-2.0-flash",
    status: "Operational",
  });


  useEffect(() => {
    systemService.getSystemInfo().then(setSystemInfo).catch(() => {});
  }, []);

  const fetchNotifications = async () => {
    try {
      const data = await notificationService.getNotifications();
      setNotifications(data || []);
    } catch (err) {
      console.error("Failed to load notifications:", err);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  const handleMarkRead = async (id) => {
    try {
      await notificationService.markAsRead(id);
      fetchNotifications();
    } catch (err) {
      console.error("Failed to mark notification as read:", err);
    }
  };

  const unreadCount = notifications.filter((n) => !n.is_read).length;
  const initials = user?.name
    ? user.name.split(" ").map((n) => n[0]).join("").toUpperCase()
    : "U";

  const getPageTitle = () => {
    switch (location.pathname) {
      case "/dashboard":
        return "Command Center";
      case "/courses":
        return "Course Catalog";
      case "/ai":
        return "AI Assistant & Multi-Agent Engine";
      case "/my-learning":
        return "My Learning Workspace";
      case "/knowledge":
        return "Knowledge Base (RAG)";
      case "/admin":
        return "Enterprise Admin Console";
      default:
        return "Workspace";
    }
  };

  return (
    <>
      <header className={`app-topbar ${collapsed ? "sidebar-collapsed" : ""}`}>
        {/* Left Metadata / Breadcrumb */}
        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: "10px", fontWeight: 400, color: "var(--text-on-cream-muted)", display: "flex", alignItems: "center", gap: "6px", letterSpacing: "-0.1px" }}>
            <span>Workspace</span> / <strong style={{ color: "var(--text-on-cream)", fontFamily: "var(--font-sans)", fontWeight: 700, fontSize: "13px" }}>{getPageTitle()}</strong>
          </div>

          {/* AI Operational Indicator */}
          <div
            title={`Active Model: ${systemService.formatModelName(systemInfo.model)}`}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              fontFamily: "var(--font-mono)",
              fontSize: "10px",
              fontWeight: 400,
              color: "var(--color-primary)",
              background: "rgba(228, 181, 146, 0.1)",
              border: "1px solid rgba(228, 181, 146, 0.2)",
              padding: "3px 10px",
              borderRadius: "var(--radius-full)",
              letterSpacing: "-0.1px",
            }}
          >
            <div className="pulse-active-dot" />
            <span>{systemInfo.provider} Operational</span>
          </div>
        </div>

        {/* Center Cmd+K Search Trigger */}
        <div className="topbar-search" onClick={() => setCmdOpen(true)}>
          <Search size={15} color="var(--text-muted)" />
          <input type="text" placeholder="Search courses, skills, agent tools..." readOnly />
          <div className="search-cmd-badge">
            <Command size={11} /> K
          </div>
        </div>

        {/* Right Actions */}
        <div className="topbar-right">

          {/* Notifications Bell */}
          <div style={{ position: "relative" }}>
            <button
              className="topbar-action-btn"
              onClick={() => setShowDrawer(!showDrawer)}
              title="Notifications"
            >
              <Bell size={17} />
              {unreadCount > 0 && (
                <span
                  style={{
                    position: "absolute",
                    top: "3px",
                    right: "3px",
                    background: "var(--color-danger)",
                    color: "white",
                    borderRadius: "50%",
                    padding: "2px 5px",
                    fontSize: "9px",
                    fontWeight: 800,
                  }}
                >
                  {unreadCount}
                </span>
              )}
            </button>

            {/* Notification Drawer Dropdown */}
            {showDrawer && (
              <div
                style={{
                  position: "absolute",
                  top: "48px",
                  right: "0",
                  width: "320px",
                  background: "var(--bg-surface)",
                  color: "var(--text-primary)",
                  borderRadius: "var(--radius-lg)",
                  boxShadow: "var(--shadow-lg)",
                  border: "1px solid var(--border-color)",
                  zIndex: 1000,
                  padding: "16px",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    borderBottom: "1px solid var(--border-color)",
                    paddingBottom: "10px",
                    marginBottom: "12px",
                    fontWeight: 700,
                    fontSize: "0.9rem",
                  }}
                >
                  <span>🔔 Notifications ({unreadCount})</span>
                  <button
                    onClick={() => setShowDrawer(false)}
                    style={{ background: "none", border: "none", cursor: "pointer", color: "var(--text-muted)" }}
                  >
                    <X size={16} />
                  </button>
                </div>

                {notifications.length === 0 ? (
                  <p style={{ fontSize: "13px", color: "var(--text-muted)", textAlign: "center", padding: "16px 0" }}>
                    No new notifications right now.
                  </p>
                ) : (
                  <div style={{ maxHeight: "260px", overflowY: "auto" }}>
                    {notifications.map((n) => (
                      <div
                        key={n.id}
                        style={{
                          background: n.is_read ? "var(--bg-primary)" : "var(--color-primary-light)",
                          padding: "10px 12px",
                          borderRadius: "var(--radius-sm)",
                          marginBottom: "8px",
                          fontSize: "13px",
                        }}
                      >
                        <div style={{ fontWeight: 700, color: "var(--text-primary)" }}>{n.title}</div>
                        <div style={{ marginTop: "2px", color: "var(--text-secondary)", fontSize: "0.82rem" }}>
                          {n.message}
                        </div>
                        {!n.is_read && (
                          <button
                            onClick={() => handleMarkRead(n.id)}
                            style={{
                              marginTop: "6px",
                              background: "var(--color-primary)",
                              color: "var(--text-inverse)",
                              border: "none",
                              borderRadius: "6px",
                              padding: "3px 8px",
                              fontSize: "11px",
                              fontWeight: 600,
                              cursor: "pointer",
                              display: "inline-flex",
                              alignItems: "center",
                              gap: "4px",
                            }}
                          >
                            <Check size={11} /> Mark read
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* User Profile Avatar */}
          <div
            className="topbar-avatar"
            onClick={() => setProfileOpen(true)}
            title={user?.name || "User Profile Settings"}
          >
            {initials}
          </div>
        </div>
      </header>

      {/* Global Command Palette & Profile Modal */}
      <CommandPalette isOpen={cmdOpen} onClose={() => setCmdOpen(false)} />
      <ProfileModal isOpen={profileOpen} onClose={() => setProfileOpen(false)} />
    </>
  );
}

export default TopBar;
