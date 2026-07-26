import React, { useState, useEffect } from "react";
import { Search, Bell, Sun, Moon, Check, X } from "lucide-react";
import useAuth from "../hooks/useAuth";
import notificationService from "../services/notificationService";
import "../styles/topBar.css";

export function TopBar({ collapsed }) {
  const { user } = useAuth();
  const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");
  const [notifications, setNotifications] = useState([]);
  const [showDrawer, setShowDrawer] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  const fetchNotifications = async () => {
    try {
      const data = await notificationService.getNotifications();
      setNotifications(data);
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

  return (
    <header className={`app-topbar ${collapsed ? "sidebar-collapsed" : ""}`}>
      {/* Search Input */}
      <div className="topbar-search">
        <Search size={18} color="var(--text-muted)" />
        <input
          type="text"
          placeholder="Search courses, skills, policies..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Topbar Actions */}
      <div className="topbar-right">
        {/* Dark Mode Toggle */}
        <button
          className="topbar-action-btn"
          onClick={toggleTheme}
          title={theme === "light" ? "Switch to Dark Mode" : "Switch to Light Mode"}
        >
          {theme === "light" ? <Moon size={18} /> : <Sun size={18} />}
        </button>

        {/* Notification Bell */}
        <div style={{ position: "relative" }}>
          <button
            className="topbar-action-btn"
            onClick={() => setShowDrawer(!showDrawer)}
            title="Notifications"
          >
            <Bell size={18} />
            {unreadCount > 0 && (
              <span
                style={{
                  position: "absolute",
                  top: "2px",
                  right: "2px",
                  background: "var(--color-danger)",
                  color: "white",
                  borderRadius: "50%",
                  padding: "2px 6px",
                  fontSize: "0.68rem",
                  fontWeight: 800,
                }}
              >
                {unreadCount}
              </span>
            )}
          </button>

          {/* Notifications Dropdown Drawer */}
          {showDrawer && (
            <div
              style={{
                position: "absolute",
                top: "50px",
                right: "0",
                width: "320px",
                background: "var(--bg-surface)",
                color: "var(--text-primary)",
                borderRadius: "var(--radius-lg)",
                boxShadow: "var(--shadow-xl)",
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
                <p style={{ fontSize: "0.85rem", color: "var(--text-muted)", textAlign: "center", padding: "12px 0" }}>
                  No notifications right now.
                </p>
              ) : (
                <div style={{ maxHeight: "260px", overflowY: "auto" }}>
                  {notifications.map((n) => (
                    <div
                      key={n.id}
                      style={{
                        background: n.is_read ? "var(--bg-primary)" : "var(--color-primary-light)",
                        padding: "10px 12px",
                        borderRadius: "var(--radius-md)",
                        marginBottom: "8px",
                        fontSize: "0.85rem",
                      }}
                    >
                      <div style={{ fontWeight: 700, color: "var(--text-primary)" }}>{n.title}</div>
                      <div style={{ marginTop: "2px", color: "var(--text-secondary)" }}>{n.message}</div>
                      {!n.is_read && (
                        <button
                          onClick={() => handleMarkRead(n.id)}
                          style={{
                            marginTop: "6px",
                            background: "var(--color-primary)",
                            color: "white",
                            border: "none",
                            borderRadius: "var(--radius-sm)",
                            padding: "4px 8px",
                            fontSize: "0.72rem",
                            cursor: "pointer",
                            display: "flex",
                            alignItems: "center",
                            gap: "4px",
                          }}
                        >
                          <Check size={12} /> Mark as read
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* User Avatar */}
        <div className="topbar-avatar" title={user?.name || "User Profile"}>
          {initials}
        </div>
      </div>
    </header>
  );
}

export default TopBar;
