import React, { useState } from "react";
import Sidebar from "./Sidebar";
import TopBar from "./TopBar";

export function AppLayout({ children }) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="app-shell">
      <Sidebar collapsed={collapsed} setCollapsed={setCollapsed} />
      <TopBar collapsed={collapsed} />
      <main className={`main-content-wrapper ${collapsed ? "sidebar-collapsed" : ""}`}>
        <div className="app-container-1400">{children}</div>
      </main>
    </div>
  );
}

export default AppLayout;
