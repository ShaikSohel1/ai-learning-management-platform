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
          <h1>🎓 My Learning Workspace</h1>
          <p style={{ color: "var(--text-secondary)", marginTop: "4px" }}>
            Track active module progress, view milestones, and download issued digital certificates.
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
                <Card key={item.id}>
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

                  <p style={{ fontSize: "0.88rem", color: "var(--text-secondary)", marginBottom: "16px", lineHeight: 1.45 }}>
                    {course.description}
                  </p>

                  <div style={{ marginTop: "auto" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.82rem", fontWeight: 600, marginBottom: "6px" }}>
                      <span>Course Completion Progress</span>
                      <span>{progress}%</span>
                    </div>

                    <div style={{ height: "8px", background: "var(--border-color)", borderRadius: "var(--radius-full)", overflow: "hidden", marginBottom: "16px" }}>
                      <div style={{ height: "100%", width: `${progress}%`, background: isDone ? "var(--color-success)" : "var(--color-primary)", borderRadius: "var(--radius-full)" }} />
                    </div>

                    <div style={{ display: "flex", gap: "10px" }}>
                      {!isDone ? (
                        <Button icon={PlayCircle} style={{ width: "100%" }} onClick={() => handleUpdateProgress(item.id, progress)}>
                          Advance Progress (+25%)
                        </Button>
                      ) : (
                        <Button variant="secondary" icon={ShieldCheck} style={{ width: "100%" }} onClick={() => handleViewCertificate(item.id)}>
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
          <div className="modal-backdrop">
            <div className="modal-content" style={{ maxWidth: "600px" }}>
              <div style={{ textAlign: "center", borderBottom: "1px solid var(--border-color)", paddingBottom: "16px", marginBottom: "16px" }}>
                <Award size={42} color="var(--color-primary)" />
                <h2 style={{ fontSize: "1.5rem", fontWeight: 800, marginTop: "8px" }}>
                  Digital Certificate of Accomplishment
                </h2>
                <Badge variant="success">Credential #{selectedCert.certificate_number || "CERT-9981"}</Badge>
              </div>

              <div style={{ padding: "16px", background: "var(--bg-primary)", borderRadius: "var(--radius-md)", marginBottom: "20px", fontSize: "0.95rem", lineHeight: 1.6 }}>
                This certifies that <strong>{selectedCert.user_name || "Learner"}</strong> has successfully completed the course:
                <h3 style={{ color: "var(--color-primary)", margin: "8px 0" }}>{selectedCert.course_title}</h3>
                Issued on {new Date(selectedCert.issued_at || Date.now()).toLocaleDateString()}.
              </div>

              <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}>
                <Button variant="outline" onClick={() => setSelectedCert(null)}>
                  Close
                </Button>
                <Button icon={Download} onClick={() => window.print()}>
                  Print / Download PDF
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}

export default MyLearning;
