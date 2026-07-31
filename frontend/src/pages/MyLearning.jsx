import React, { useState, useEffect } from "react";
import {
  GraduationCap,
  Award,
  PlayCircle,
  CheckCircle,
  Download,
  ShieldCheck,
  Calendar,
  Layers,
  Printer,
  X,
  Sparkles,
} from "lucide-react";

import AppLayout from "../components/AppLayout";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Badge from "../components/common/Badge";
import EmptyState from "../components/common/EmptyState";
import LoadingSkeleton from "../components/common/LoadingSkeleton";
import enrollmentService from "../services/enrollmentService";
import "../styles/myLearning.css";

function MyLearning() {
  const [enrollments, setEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCert, setSelectedCert] = useState(null);

  const loadEnrollments = async () => {
    try {
      setLoading(true);
      const data = await enrollmentService.getMyEnrollments();
      setEnrollments(data || []);
    } catch (err) {
      console.error("Failed to load enrollments:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEnrollments();
  }, []);

  const handleUpdateProgress = async (id, currentProgress) => {
    const nextProgress = Math.min(100, currentProgress + 25);
    try {
      if (nextProgress >= 100) {
        await enrollmentService.completeCourse(id);
      } else {
        await enrollmentService.updateProgress(id, nextProgress);
      }
      loadEnrollments();
    } catch (err) {
      alert(err.response?.data?.detail || "Could not update course progress.");
    }
  };

  const handleViewCertificate = async (enrollmentId) => {
    try {
      const certData = await enrollmentService.getCertificate(enrollmentId);
      setSelectedCert(certData);
    } catch (err) {
      alert(err.response?.data?.detail || "Could not fetch certificate.");
    }
  };

  return (
    <AppLayout>
      <div className="mylearning-container">
        {/* Header Bar */}
        <div style={{ marginBottom: "24px" }}>
          <h1 style={{ fontSize: "1.75rem", fontWeight: 800 }}>🎓 My Learning Workspace</h1>
          <p style={{ color: "var(--text-secondary)", marginTop: "4px" }}>
            Track active module progress, view milestones, and inspect digital certificates.
          </p>
        </div>

        {loading ? (
          <LoadingSkeleton height="180px" count={3} />
        ) : enrollments.length === 0 ? (
          <EmptyState
            icon={GraduationCap}
            title="No Course Enrollments"
            description="You have not enrolled in any learning paths yet. Explore the Course Catalog!"
          />
        ) : (
          <div className="mylearning-grid">
            {enrollments.map((item) => {
              const course = item.course || {};
              const progress = item.progress_percentage || 0;
              const isDone = item.status === "COMPLETED";

              return (
                <Card key={item.id} hoverEffect style={{ display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
                  <div>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
                      <div>
                        <Badge variant={isDone ? "success" : "primary"}>
                          {isDone ? "Completed" : "In Progress"}
                        </Badge>
                        <h3 style={{ fontSize: "1.15rem", fontWeight: 700, marginTop: "8px" }}>
                          {course.title || "Course"}
                        </h3>
                      </div>

                      <span style={{ fontSize: "0.82rem", color: "var(--text-muted)", fontWeight: 600 }}>
                        {course.category || "General"}
                      </span>
                    </div>

                    <p style={{ fontSize: "0.88rem", color: "var(--text-secondary)", marginBottom: "16px", lineHeight: 1.5 }}>
                      {course.description}
                    </p>
                  </div>

                  <div style={{ marginTop: "auto" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.82rem", fontWeight: 600, marginBottom: "6px" }}>
                      <span>Course Completion Progress</span>
                      <span>{progress}%</span>
                    </div>

                    <div style={{ height: "8px", background: "var(--border-color)", borderRadius: "var(--radius-full)", overflow: "hidden", marginBottom: "16px" }}>
                      <div style={{ height: "100%", width: `${progress}%`, background: isDone ? "var(--color-success)" : "var(--gradient-cta)", borderRadius: "var(--radius-full)" }} />
                    </div>

                    <div style={{ display: "flex", gap: "10px" }}>
                      {!isDone ? (
                        <Button icon={PlayCircle} style={{ width: "100%" }} onClick={() => handleUpdateProgress(item.id, progress)}>
                          Advance Progress (+25%)
                        </Button>
                      ) : (
                        <Button variant="glow" icon={ShieldCheck} style={{ width: "100%" }} onClick={() => handleViewCertificate(item.id)}>
                          View Digital Certificate
                        </Button>
                      )}
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        )}

        {/* Certificate Modal */}
        {selectedCert && (
          <div className="modal-backdrop" onClick={() => setSelectedCert(null)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: "600px" }}>
              <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "8px" }}>
                <button onClick={() => setSelectedCert(null)} style={{ background: "none", border: "none", color: "var(--text-muted)", cursor: "pointer" }}>
                  <X size={20} />
                </button>
              </div>

              <div className="certificate-card-preview">
                <div className="certificate-seal">
                  <Award size={32} />
                </div>
                <Badge variant="glow" icon={Sparkles} style={{ marginBottom: "12px" }}>
                  Verified Enterprise Certificate
                </Badge>
                <h2 style={{ fontSize: "1.6rem", fontWeight: 800, color: "var(--text-primary)" }}>
                  Digital Certificate of Accomplishment
                </h2>
                <span style={{ fontSize: "0.82rem", color: "var(--text-muted)", fontWeight: 600, display: "block", marginTop: "4px" }}>
                  Credential ID: #{selectedCert.certificate_number || "CERT-9981"}
                </span>

                <div style={{ margin: "20px 0", padding: "16px", background: "var(--bg-surface)", borderRadius: "var(--radius-md)", border: "1px solid var(--border-color)", fontSize: "0.95rem", lineHeight: 1.6 }}>
                  This certifies that <strong>{selectedCert.user_name || "Learner"}</strong> has successfully completed the course:
                  <h3 style={{ color: "var(--color-primary)", margin: "8px 0", fontSize: "1.2rem", fontWeight: 800 }}>
                    {selectedCert.course_title}
                  </h3>
                  Issued on {new Date(selectedCert.issued_at || Date.now()).toLocaleDateString()}.
                </div>

                <div style={{ display: "flex", justifyContent: "center", gap: "12px", marginTop: "24px" }}>
                  <Button variant="outline" onClick={() => setSelectedCert(null)}>
                    Close Preview
                  </Button>
                  <Button icon={Printer} variant="glow" onClick={() => window.print()}>
                    Print / Export PDF
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}

export default MyLearning;
