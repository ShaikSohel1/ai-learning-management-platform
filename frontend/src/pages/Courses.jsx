import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import CourseTable from "../components/CourseTable";
import CourseForm from "../components/CourseForm";

import {
  getCourses,
  createCourse,
  updateCourse,
  deleteCourse,
} from "../services/courseService";
import enrollmentService from "../services/enrollmentService";

import "../styles/courses.css";

function Courses() {
  const [courses, setCourses] = useState([]);
  const [enrolledCourseIds, setEnrolledCourseIds] = useState([]);
  const [loading, setLoading] = useState(false);

  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [sort, setSort] = useState("id");

  const [page, setPage] = useState(1);
  const limit = 5;

  const [editingCourse, setEditingCourse] = useState(null);

  const loadEnrollments = async () => {
    try {
      const data = await enrollmentService.getMyEnrollments();
      const ids = data.map((e) => e.course_id);
      setEnrolledCourseIds(ids);
    } catch (error) {
      console.error("Failed to load user enrollments:", error);
    }
  };

  const loadCourses = async () => {
    try {
      setLoading(true);

      const data = await getCourses({
        search,
        category,
        difficulty,
        sort,
        page,
        limit,
      });

      setCourses(data);
    } catch (error) {
      console.error(error);
      alert(
        error.response?.data?.detail ||
          "Failed to fetch courses."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCourses();
    loadEnrollments();
  }, [search, category, difficulty, sort, page]);

  const handleEnroll = async (courseId) => {
    try {
      await enrollmentService.enrollInCourse(courseId);
      loadEnrollments();
      alert("Successfully enrolled in course!");
    } catch (error) {
      console.error("Enrollment failed:", error);
      alert(
        error.response?.data?.detail || "Unable to enroll in course."
      );
    }
  };

  const handleCreate = async (course) => {
    try {
      await createCourse(course);
      loadCourses();
    } catch (error) {
      console.error(error);
      alert(
        error.response?.data?.detail ||
          "Unable to create course."
      );
    }
  };

  const handleUpdate = async (course) => {
    try {
      await updateCourse(editingCourse.id, course);

      setEditingCourse(null);

      loadCourses();
    } catch (error) {
      console.error(error);
      alert(
        error.response?.data?.detail ||
          "Unable to update course."
      );
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this course?")) return;

    try {
      await deleteCourse(id);

      loadCourses();
    } catch (error) {
      console.error(error);
      alert(
        error.response?.data?.detail ||
          "Unable to delete course."
      );
    }
  };

  return (
    <>
      <Navbar />

      <div className="courses-page">
        <div className="courses-header">
          <h2>Course Management</h2>

          <div className="filters">
            <input
              type="text"
              placeholder="Search..."
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
            />

            <select
              value={category}
              onChange={(e) => {
                setCategory(e.target.value);
                setPage(1);
              }}
            >
              <option value="">All Categories</option>
              <option value="Programming">Programming</option>
              <option value="AI">AI</option>
              <option value="Cloud">Cloud</option>
              <option value="Database">Database</option>
            </select>

            <select
              value={difficulty}
              onChange={(e) => {
                setDifficulty(e.target.value);
                setPage(1);
              }}
            >
              <option value="">All Levels</option>
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>

            <select
              value={sort}
              onChange={(e) => setSort(e.target.value)}
            >
              <option value="id">Newest</option>
              <option value="title">Title</option>
              <option value="duration">Duration</option>
              <option value="difficulty">Difficulty</option>
            </select>
          </div>
        </div>

        <CourseForm
          editingCourse={editingCourse}
          onCreate={handleCreate}
          onUpdate={handleUpdate}
        />

        {loading ? (
          <h2 style={{ textAlign: "center" }}>
            Loading Courses...
          </h2>
        ) : (
          <>
            <CourseTable
              courses={courses}
              onEdit={setEditingCourse}
              onDelete={handleDelete}
              enrolledCourseIds={enrolledCourseIds}
              onEnroll={handleEnroll}
            />

            <div className="pagination">
              <button
                disabled={page === 1}
                onClick={() => setPage(page - 1)}
              >
                Previous
              </button>

              <span>Page {page}</span>

              <button
                disabled={courses.length < limit}
                onClick={() => setPage(page + 1)}
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </>
  );
}

export default Courses;