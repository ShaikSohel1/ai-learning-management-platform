import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import enrollmentService from "../services/enrollmentService";
import "../styles/myLearning.css";

function MyLearning() {
  const [enrollments, setEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("ALL"); // 'ALL' | 'IN_PROGRESS' | 'COMPLETED' | 'NOT_STARTED'

  // Certificate Modal State
  const [selectedCert, setSelectedCert] = useState(null);
  const [loadingCert, setLoadingCert] = useState(false);

  const loadEnrollments = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await enrollmentService.getMyEnrollments();
      setEnrollments(data);
    } catch (err) {
      console.error("Failed to load enrollments:", err);
      setError(
        err.response?.data?.detail || "Failed to load your enrolled courses."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEnrollments();
  }, []);

  // Action: Start or Increase Progress
  const handleProgressUpdate = async (enrollmentId, currentProgress, increment = 25) => {
    try {
      const nextProgress = Math.min(100, currentProgress + increment);
      await enrollmentService.updateProgress(enrollmentId, nextProgress);
      loadEnrollments();
    } catch (err) {
      console.error("Failed to update progress:", err);
      alert(err.response?.data?.detail || "Could not update progress.");
    }
  };

  // Action: Complete Course
  const handleComplete = async (enrollmentId) => {
    try {
      await enrollmentService.completeCourse(enrollmentId);
      loadEnrollments();
    } catch (err) {
      console.error("Failed to complete course:", err);
      alert(err.response?.data?.detail || "Could not complete course.");
    }
  };

  // Action: Remove Enrollment
  const handleRemove = async (enrollmentId) => {
    if (!window.confirm("Are you sure you want to remove this enrollment?")) return;
    try {
      await enrollmentService.deleteEnrollment(enrollmentId);
      loadEnrollments();
    } catch (err) {
      console.error("Failed to remove enrollment:", err);
      alert(err.response?.data?.detail || "Could not remove enrollment.");
    }
  };

  // Action: Open Certificate Modal
  const handleViewCertificate = async (enrollmentId) => {
    try {
      setLoadingCert(true);
      const certData = await enrollmentService.getCertificate(enrollmentId);
      setSelectedCert(certData);
    } catch (err) {
      console.error("Failed to fetch certificate:", err);
      alert(err.response?.data?.detail || "Certificate not available.");
    } finally {
      setLoadingCert(false);
    }
  };

  // Filtered List
  const filteredEnrollments = enrollments.filter((item) => {
    if (filter === "ALL") return true;
    return item.status === filter;
  });

  // Calculate Summary Statistics
  const totalCount = enrollments.length;
  const inProgressCount = enrollments.filter((e) => e.status === "IN_PROGRESS").length;
  const completedCount = enrollments.filter((e) => e.status === "COMPLETED").length;

  return (
    <div>
      <Navbar />

      <div className="my-learning-container">
        {/* Header Stats */}
        <div className="learning-header">
          <div className="learning-header-text">
            <h1>🎓 My Learning Workspace</h1>
            <p>Track your active courses, skill acquisition milestones, and certificates.</p>
          </div>

          <div className="stats-pills">
            <div className="stat-pill">
              <div className="num">{totalCount}</div>
              <div className="label">Total Enrolled</div>
            </div>
            <div className="stat-pill">
              <div className="num">{inProgressCount}</div>
              <div className="label">In Progress</div>
            </div>
            <div className="stat-pill">
              <div className="num">{completedCount}</div>
              <div className="label">Completed</div>
            </div>
          </div>
        </div>

        {/* Filter Tabs */}
        <div className="learning-filter-tabs">
          <button
            className={`filter-tab-btn ${filter === "ALL" ? "active" : ""}`}
            onClick={() => setFilter("ALL")}
          >
            All Courses ({totalCount})
          </button>
          <button
            className={`filter-tab-btn ${filter === "IN_PROGRESS" ? "active" : ""}`}
            onClick={() => setFilter("IN_PROGRESS")}
          >
            In Progress ({inProgressCount})
          </button>
          <button
            className={`filter-tab-btn ${filter === "COMPLETED" ? "active" : ""}`}
            onClick={() => setFilter("COMPLETED")}
          >
            Completed ({completedCount})
          </button>
        </div>

        {/* Error State */}
        {error && <div className="error-banner">{error}</div>}

        {/* Loading State */}
        {loading ? (
          <div className="empty-learning-state">
            <h3>Loading Your Enrolled Courses...</h3>
          </div>
        ) : filteredEnrollments.length === 0 ? (
          /* Empty State */
          <div className="empty-learning-state">
            <h3>No Enrolled Courses Found</h3>
            <p>Explore our Course Catalog or generate an AI Learning Path to start learning.</p>
          </div>
        ) : (
          /* Course Cards Grid */
          <div className="my-learning-grid">
            {filteredEnrollments.map((item) => {
              const course = item.course || {};
              const progress = item.progress_percentage || 0;
              const status = item.status || "NOT_STARTED";

              return (
                <div key={item.id} className="my-course-card">
                  <div className="card-top">
                    <span className={`card-status-badge status-${status}`}>
                      {status === "NOT_STARTED" && "Not Started"}
                      {status === "IN_PROGRESS" && "In Progress"}
                      {status === "COMPLETED" && "Completed 🏆"}
                    </span>

                    <h3 className="course-card-title">{course.title || "Course"}</h3>

                    <div className="course-card-meta">
                      <span>🏷️ {course.category || "General"}</span>
                      <span>📊 {course.difficulty || "Intermediate"}</span>
                      <span>⏱️ {course.duration || 10} hrs</span>
                    </div>

                    <p className="course-card-desc">
                      {course.description || "Interactive course modules."}
                    </p>
                  </div>

                  <div>
                    {/* Progress Bar */}
                    <div className="progress-container">
                      <div className="progress-header">
                        <span>Course Progress</span>
                        <span>{progress}%</span>
                      </div>
                      <div className="progress-track">
                        <div
                          className={`progress-fill ${status === "COMPLETED" ? "completed" : ""}`}
                          style={{ width: `${progress}%` }}
                        ></div>
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="card-actions">
                      {status === "NOT_STARTED" && (
                        <button
                          className="btn-learn btn-start"
                          onClick={() => handleProgressUpdate(item.id, progress, 15)}
                        >
                          ▶️ Start Learning
                        </button>
                      )}

                      {status === "IN_PROGRESS" && (
                        <div style={{ display: "flex", gap: "8px" }}>
                          <button
                            className="btn-learn btn-continue"
                            style={{ flex: 1 }}
                            onClick={() => handleProgressUpdate(item.id, progress, 25)}
                          >
                            ⚡ Continue (+25%)
                          </button>

                          <button
                            className="btn-learn btn-complete-course"
                            style={{ flex: 1 }}
                            onClick={() => handleComplete(item.id)}
                          >
                            ✅ Complete
                          </button>
                        </div>
                      )}

                      {status === "COMPLETED" && (
                        <button
                          className="btn-learn btn-view-cert"
                          onClick={() => handleViewCertificate(item.id)}
                          disabled={loadingCert}
                        >
                          📜 View Certificate
                        </button>
                      )}

                      <button
                        className="btn-remove-enrollment"
                        onClick={() => handleRemove(item.id)}
                      >
                        Remove Enrollment
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Digital Certificate Modal */}
        {selectedCert && (
          <div className="modal-overlay" onClick={() => setSelectedCert(null)}>
            <div
              className="certificate-modal"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="certificate-frame">
                <div className="cert-logo">AI LMS ENTERPRISE</div>
                <div className="cert-title">Certificate of Completion</div>

                <div className="cert-subtitle">This is proudly presented to</div>
                <div className="cert-name">
                  {selectedCert.user_name || "Learner"}
                </div>

                <div className="cert-body">
                  for successfully completing all curriculum requirements and practical assessments for
                  <br />
                  <span className="cert-course-title">"{selectedCert.course_title}"</span>
                </div>

                <div className="cert-footer">
                  <div className="cert-meta-item">
                    <strong>Issued Date:</strong>{" "}
                    {new Date(selectedCert.issued_at).toLocaleDateString()}
                    <br />
                    <strong>Certificate ID:</strong> {selectedCert.certificate_number}
                  </div>

                  <div className="cert-meta-item" style={{ textAlign: "right" }}>
                    <div
                      style={{
                        fontFamily: "Georgia, serif",
                        fontStyle: "italic",
                        fontSize: "1.2rem",
                        color: "#4338ca",
                        borderBottom: "1px solid #cbd5e1",
                        paddingBottom: "4px",
                      }}
                    >
                      Enterprise AI L&D Committee
                    </div>
                    <strong>Authorized Signatory</strong>
                  </div>
                </div>
              </div>

              <div className="cert-actions">
                <button
                  className="btn-cert-action btn-print"
                  onClick={() => window.print()}
                >
                  🖨️ Print / Save PDF
                </button>
                <button
                  className="btn-cert-action btn-close-modal"
                  onClick={() => setSelectedCert(null)}
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default MyLearning;
