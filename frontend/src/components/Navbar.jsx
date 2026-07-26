import { Link, useLocation, useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

function Navbar() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

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

      <div className="navbar-user">
        <span>{user?.name}</span>
        <button onClick={handleLogout}>Logout</button>
      </div>
    </nav>
  );
}

export default Navbar;