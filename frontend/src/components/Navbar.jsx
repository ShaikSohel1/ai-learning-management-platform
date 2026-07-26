import { useState, useEffect } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import notificationService from "../services/notificationService";

function Navbar() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [notifications, setNotifications] = useState([]);
  const [showDrawer, setShowDrawer] = useState(false);

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

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const handleMarkRead = async (id) => {
    try {
      await notificationService.markAsRead(id);
      fetchNotifications();
    } catch (err) {
      console.error("Failed to mark notification as read:", err);
    }
  };

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <h2>AI LMS</h2>
      </div>

      <div className="navbar-links">
        <Link
          to="/dashboard"
          className={location.pathname === "/dashboard" ? "active" : ""}
        >
          Dashboard
        </Link>

        <Link
          to="/courses"
          className={location.pathname === "/courses" ? "active" : ""}
        >
          Courses
        </Link>

        <Link
          to="/ai"
          className={location.pathname === "/ai" ? "active" : ""}
        >
          ✨ AI Assistant
        </Link>

        <Link
          to="/my-learning"
          className={location.pathname === "/my-learning" ? "active" : ""}
        >
          🎓 My Learning
        </Link>

        <Link
          to="/knowledge"
          className={location.pathname === "/knowledge" ? "active" : ""}
        >
          📖 Knowledge Base
        </Link>
      </div>

      <div className="navbar-user" style={{ position: "relative" }}>
        {/* Notification Bell */}
        <button
          onClick={() => setShowDrawer(!showDrawer)}
          style={{
            background: "transparent",
            border: "none",
            color: "white",
            fontSize: "1.2rem",
            cursor: "pointer",
            position: "relative",
            marginRight: "15px",
          }}
        >
          🔔
          {unreadCount > 0 && (
            <span
              style={{
                position: "absolute",
                top: "-4px",
                right: "-6px",
                background: "#ef4444",
                color: "white",
                borderRadius: "50%",
                padding: "2px 6px",
                fontSize: "0.7rem",
                fontWeight: 700,
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
              top: "45px",
              right: "80px",
              width: "320px",
              background: "white",
              color: "#1e293b",
              borderRadius: "12px",
              boxShadow: "0 10px 25px rgba(0,0,0,0.15)",
              border: "1px solid #cbd5e1",
              zIndex: 1000,
              padding: "15px",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                borderBottom: "1px solid #e2e8f0",
                paddingBottom: "8px",
                marginBottom: "10px",
                fontWeight: 700,
              }}
            >
              <span>🔔 Notifications ({unreadCount} unread)</span>
              <button
                onClick={() => setShowDrawer(false)}
                style={{ background: "none", border: "none", cursor: "pointer", fontSize: "0.9rem" }}
              >
                ✕
              </button>
            </div>

            {notifications.length === 0 ? (
              <p style={{ fontSize: "0.85rem", color: "#64748b", textAlign: "center", padding: "10px 0" }}>
                No notifications right now.
              </p>
            ) : (
              <div style={{ maxHeight: "250px", overflowY: "auto" }}>
                {notifications.map((n) => (
                  <div
                    key={n.id}
                    style={{
                      background: n.is_read ? "#f8fafc" : "#eff6ff",
                      padding: "10px",
                      borderRadius: "8px",
                      marginBottom: "8px",
                      fontSize: "0.85rem",
                    }}
                  >
                    <div style={{ fontWeight: 700, color: "#1e40af" }}>{n.title}</div>
                    <div style={{ marginTop: "2px", color: "#334155" }}>{n.message}</div>
                    {!n.is_read && (
                      <button
                        onClick={() => handleMarkRead(n.id)}
                        style={{
                          marginTop: "6px",
                          background: "#2563eb",
                          color: "white",
                          border: "none",
                          borderRadius: "4px",
                          padding: "2px 8px",
                          fontSize: "0.75rem",
                          cursor: "pointer",
                        }}
                      >
                        Mark as read
                      </button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        <span>{user?.name}</span>
        <button onClick={handleLogout}>Logout</button>
      </div>
    </nav>
  );
}

export default Navbar;