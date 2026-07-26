import { useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

import "../styles/dashboard.css";

function Dashboard() {
  const navigate = useNavigate();

  const {
    user,
    logout,
  } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="dashboard">

      <header className="dashboard-header">
        <h1>AI Learning Management System</h1>

        <button
          className="logout-btn"
          onClick={handleLogout}
        >
          Logout
        </button>
      </header>

      <section className="welcome-card">

        <h2>
          Welcome, {user?.name || "User"} 👋
        </h2>

        <div className="user-details">

          <p>
            <strong>Email:</strong>{" "}
            {user?.email}
          </p>

          <p>
            <strong>Role:</strong>{" "}
            {user?.role}
          </p>

          <p>
            <strong>Department:</strong>{" "}
            {user?.department}
          </p>

          <p>
            <strong>Designation:</strong>{" "}
            {user?.designation}
          </p>

        </div>

      </section>

      <section className="dashboard-actions">

        <button
          className="primary-btn"
          onClick={() => navigate("/courses")}
        >
          Manage Courses
        </button>

      </section>

    </div>
  );
}

export default Dashboard;