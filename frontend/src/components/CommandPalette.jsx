import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Search, Command, BookOpen, Sparkles, Database, LayoutDashboard, Settings, GraduationCap, X, ArrowRight } from "lucide-react";

export function CommandPalette({ isOpen, onClose }) {
  const [query, setQuery] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        if (isOpen) {
          onClose();
        } else {
          // Open handled by parent or custom event
        }
      }
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const actions = [
    { title: "Dashboard Overview", subtitle: "View metrics, streak, and charts", path: "/dashboard", icon: LayoutDashboard, category: "Navigation" },
    { title: "AI Learning Assistant", subtitle: "Ask Gemini multi-agent platform", path: "/ai", icon: Sparkles, category: "AI Tools" },
    { title: "Course Catalog", subtitle: "Browse enterprise courses & labs", path: "/courses", icon: BookOpen, category: "Learning" },
    { title: "My Learning Workspace", subtitle: "Track progress & certificates", path: "/my-learning", icon: GraduationCap, category: "Learning" },
    { title: "Knowledge Base (RAG)", subtitle: "Ingest & search ChromaDB vector store", path: "/knowledge", icon: Database, category: "AI Tools" },
    { title: "Enterprise Admin Panel", subtitle: "Monitor health, API metrics & users", path: "/admin", icon: Settings, category: "Admin" },
  ];

  const filtered = actions.filter(
    (a) =>
      a.title.toLowerCase().includes(query.toLowerCase()) ||
      a.subtitle.toLowerCase().includes(query.toLowerCase()) ||
      a.category.toLowerCase().includes(query.toLowerCase())
  );

  const handleSelect = (path) => {
    navigate(path);
    onClose();
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
        style={{
          maxWidth: "600px",
          padding: "0",
          overflow: "hidden",
          borderRadius: "var(--radius-lg)",
          boxShadow: "var(--shadow-lg)",
          border: "1px solid var(--border-color-active)",
        }}
      >
        {/* Search Input Bar */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            padding: "16px 20px",
            borderBottom: "1px solid var(--border-color)",
            background: "var(--bg-surface)",
          }}
        >
          <Search size={20} color="var(--color-primary)" />
          <input
            type="text"
            placeholder="Type a command or search workspace..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
            style={{
              flex: 1,
              background: "transparent",
              border: "none",
              outline: "none",
              color: "var(--text-primary)",
              fontSize: "1rem",
              fontFamily: "var(--font-sans)",
            }}
          />
          <button
            onClick={onClose}
            style={{
              background: "transparent",
              border: "none",
              color: "var(--text-muted)",
              cursor: "pointer",
            }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Results Stream */}
        <div style={{ maxHeight: "360px", overflowY: "auto", padding: "12px 16px" }}>
          {filtered.length === 0 ? (
            <div style={{ padding: "32px", textAlign: "center", color: "var(--text-muted)", fontSize: "0.9rem" }}>
              No matching commands or pages found.
            </div>
          ) : (
            filtered.map((item, idx) => {
              const Icon = item.icon;
              return (
                <div
                  key={idx}
                  onClick={() => handleSelect(item.path)}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    padding: "12px 14px",
                    borderRadius: "var(--radius-md)",
                    cursor: "pointer",
                    transition: "background 0.15s ease",
                    marginBottom: "4px",
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = "var(--bg-surface-hover)")}
                  onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                    <div
                      style={{
                        width: "36px",
                        height: "36px",
                        borderRadius: "var(--radius-sm)",
                        background: "var(--color-primary-light)",
                        color: "var(--color-primary)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }}
                    >
                      <Icon size={18} />
                    </div>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: "0.92rem", color: "var(--text-primary)" }}>
                        {item.title}
                      </div>
                      <div style={{ fontSize: "0.78rem", color: "var(--text-muted)" }}>{item.subtitle}</div>
                    </div>
                  </div>

                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    <span style={{ fontSize: "0.72rem", background: "var(--border-color)", padding: "2px 8px", borderRadius: "10px", color: "var(--text-muted)", fontWeight: 600 }}>
                      {item.category}
                    </span>
                    <ArrowRight size={14} color="var(--text-muted)" />
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Footer Bar */}
        <div
          style={{
            padding: "10px 20px",
            borderTop: "1px solid var(--border-color)",
            background: "rgba(0,0,0,0.2)",
            display: "flex",
            justifyContent: "space-between",
            fontSize: "0.76rem",
            color: "var(--text-muted)",
          }}
        >
          <span>Use <strong>↑ ↓</strong> to navigate</span>
          <span>Press <strong>ESC</strong> to dismiss</span>
        </div>
      </div>
    </div>
  );
}

export default CommandPalette;
