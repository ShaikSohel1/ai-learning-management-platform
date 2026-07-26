import React, { useState, useEffect } from "react";
import {
  BookOpen,
  Search,
  Plus,
  Edit2,
  Trash2,
  Clock,
  BarChart,
  User,
  Sparkles,
  CheckCircle,
} from "lucide-react";

import AppLayout from "../components/AppLayout";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import Badge from "../components/common/Badge";
import EmptyState from "../components/common/EmptyState";
import LoadingSkeleton from "../components/common/LoadingSkeleton";
import useAuth from "../hooks/useAuth";
import courseService from "../services/courseService";
import enrollmentService from "../services/enrollmentService";
import "../styles/courses.css";

function Courses() {
  const { user } = useAuth();
  const isAdmin = user?.role?.toLowerCase() === "admin";

  const [courses, setCourses] = useState([]);
  const [userEnrollments, setUserEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [difficulty, setDifficulty] = useState("");

  // Modal State
  const [showModal, setShowModal] = useState(false);
  const [editCourse, setEditCourse] = useState(null);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    category: "",
    duration: "",
    difficulty: "Beginner",
  });

  const loadData = async () => {
    try {
      setLoading(true);
      const [coursesData, enrollmentsData] = await Promise.all([
        courseService.getCourses({ search, category, difficulty, limit: 50 }),
        enrollmentService.getMyEnrollments(),
      ]);
      setCourses(coursesData.courses || []);
      setUserEnrollments(enrollmentsData || []);
    } catch (err) {
      console.error("Error loading courses:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [search, category, difficulty]);

  // Handlers
  const handleOpenAddModal = () => {
    setEditCourse(null);
    setFormData({ title: "", description: "", category: "", duration: "", difficulty: "Beginner" });
    setShowModal(true);
  };

  const handleOpenEditModal = (course) => {
    setEditCourse(course);
    setFormData({
      title: course.title,
      description: course.description,
      category: course.category,
      duration: course.duration,
      difficulty: course.difficulty,
    });
    setShowModal(true);
  };

  const handleSaveCourse = async (e) => {
    e.preventDefault();
    try {
      if (editCourse) {
        await courseService.updateCourse(editCourse.id, formData);
      } else {
        await courseService.createCourse(formData);
      }
      setShowModal(false);
      loadData();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to save course.");
    }
  };

  const handleDeleteCourse = async (courseId, title) => {
    if (!window.confirm(`Delete course "${title}"?`)) return;
    try {
      await courseService.deleteCourse(courseId);
      loadData();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to delete course.");
    }
  };

  const handleEnroll = async (courseId) => {
    try {
      await enrollmentService.enrollUser(courseId);
      alert("Enrolled successfully!");
      loadData();
    } catch (err) {
      alert(err.response?.data?.detail || "Could not complete enrollment.");
    }
  };

  const isEnrolled = (courseId) => {
    return userEnrollments.some((e) => e.course_id === courseId);
  };

  return (
    <AppLayout>
      <div className="courses-container">
        {/* Header Bar */}
        <div className="courses-header-bar">
          <div>
            <h1>📚 LMS Course Catalog</h1>
            <p style={{ color: "var(--text-secondary)", marginTop: "4px" }}>
              Explore enterprise learning paths, AI-matched courses, and technical labs.
            </p>
          </div>

          {isAdmin && (
            <Button icon={Plus} onClick={handleOpenAddModal}>
              Create New Course
            </Button>
          )}
        </div>

        {/* Filter Toolbar */}
        <Card style={{ marginBottom: "24px" }}>
          <div className="courses-filter-bar">
            <div className="filter-input-box">
              <Search size={18} color="var(--text-muted)" />
              <input
                type="text"
                placeholder="Filter courses by title..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>

            <select className="filter-select" value={category} onChange={(e) => setCategory(e.target.value)}>
              <option value="">All Categories</option>
              <option value="Programming">Programming</option>
              <option value="Database">Database</option>
              <option value="DevOps">DevOps</option>
              <option value="Cloud">Cloud</option>
            </select>

            <select className="filter-select" value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
              <option value="">All Difficulties</option>
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>
          </div>
        </Card>

        {/* Course Cards Responsive Grid */}
        {loading ? (
          <LoadingSkeleton height="220px" count={3} />
        ) : courses.length === 0 ? (
          <EmptyState
            icon={BookOpen}
            title="No Courses Found"
            description="No courses match your current search or filter criteria."
          />
        ) : (
          <div className="courses-grid">
            {courses.map((course, idx) => {
              const enrolled = isEnrolled(course.id);
              const matchPercent = 90 + ((idx * 3) % 9); // AI Match Score

              return (
                <Card key={course.id} style={{ display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
                  <div>
                    {/* Course Image Header Banner */}
                    <div className="course-card-banner">
                      <Badge variant="purple" icon={Sparkles}>
                        {matchPercent}% AI Match
                      </Badge>
                      <Badge variant="primary">{course.category || "General"}</Badge>
                    </div>

                    <h3 className="course-card-title">{course.title}</h3>
                    <p className="course-card-desc">{course.description}</p>

                    <div className="course-card-meta">
                      <span>
                        <Clock size={14} /> {course.duration || "10"} hrs
                      </span>
                      <span>
                        <BarChart size={14} /> {course.difficulty || "Intermediate"}
                      </span>
                      <span>
                        <User size={14} /> Senior Architect
                      </span>
                    </div>
                  </div>

                  <div className="course-card-actions">
                    {enrolled ? (
                      <Button variant="secondary" icon={CheckCircle} disabled style={{ width: "100%" }}>
                        Enrolled
                      </Button>
                    ) : (
                      <Button style={{ width: "100%" }} onClick={() => handleEnroll(course.id)}>
                        Enroll Now
                      </Button>
                    )}

                    {isAdmin && (
                      <div style={{ display: "flex", gap: "8px", marginTop: "10px" }}>
                        <Button variant="outline" size="sm" icon={Edit2} onClick={() => handleOpenEditModal(course)}>
                          Edit
                        </Button>
                        <Button variant="danger" size="sm" icon={Trash2} onClick={() => handleDeleteCourse(course.id, course.title)}>
                          Delete
                        </Button>
                      </div>
                    )}
                  </div>
                </Card>
              );
            })}
          </div>
        )}

        {/* Modal: Create / Edit Course */}
        {showModal && (
          <div className="modal-backdrop">
            <div className="modal-content">
              <h3>{editCourse ? "Edit Course" : "Create New Course"}</h3>
              <form onSubmit={handleSaveCourse} style={{ marginTop: "16px" }}>
                <div style={{ marginBottom: "12px" }}>
                  <label style={{ fontSize: "0.85rem", fontWeight: 600 }}>Title</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    required
                  />
                </div>

                <div style={{ marginBottom: "12px" }}>
                  <label style={{ fontSize: "0.85rem", fontWeight: 600 }}>Description</label>
                  <textarea
                    className="form-control"
                    rows={3}
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    required
                  />
                </div>

                <div style={{ display: "flex", gap: "10px", marginBottom: "16px" }}>
                  <div style={{ flex: 1 }}>
                    <label style={{ fontSize: "0.85rem", fontWeight: 600 }}>Category</label>
                    <input
                      type="text"
                      className="form-control"
                      value={formData.category}
                      onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                      required
                    />
                  </div>

                  <div style={{ flex: 1 }}>
                    <label style={{ fontSize: "0.85rem", fontWeight: 600 }}>Duration (hrs)</label>
                    <input
                      type="number"
                      className="form-control"
                      value={formData.duration}
                      onChange={(e) => setFormData({ ...formData, duration: e.target.value })}
                      required
                    />
                  </div>
                </div>

                <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}>
                  <Button variant="outline" onClick={() => setShowModal(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">Save Course</Button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}

export default Courses;