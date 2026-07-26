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
        {children}
      </main>
    </div>
  );
}

export default AppLayout;
