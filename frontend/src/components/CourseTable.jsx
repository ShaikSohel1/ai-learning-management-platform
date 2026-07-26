function CourseTable({ courses, onEdit, onDelete, enrolledCourseIds = [], onEnroll }) {
  if (courses.length === 0) {
    return (
      <div className="no-courses">
        <h3>No Courses Found</h3>
      </div>
    );
  }

  return (
    <table className="course-table">
      <thead>
        <tr>
          <th>Title</th>
          <th>Category</th>
          <th>Duration (hrs)</th>
          <th>Difficulty</th>
          <th>Enrollment</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        {courses.map((course) => {
          const isEnrolled = enrolledCourseIds.includes(course.id);

          return (
            <tr key={course.id}>
              <td>{course.title}</td>
              <td>{course.category}</td>
              <td>{course.duration}</td>
              <td>{course.difficulty}</td>

              <td>
                {isEnrolled ? (
                  <span
                    style={{
                      background: "#dcfce7",
                      color: "#15803d",
                      padding: "4px 10px",
                      borderRadius: "12px",
                      fontSize: "0.8rem",
                      fontWeight: "700",
                    }}
                  >
                    ✓ Already Enrolled
                  </span>
                ) : (
                  <button
                    style={{
                      background: "#2563eb",
                      color: "white",
                      border: "none",
                      padding: "6px 12px",
                      borderRadius: "6px",
                      fontWeight: "600",
                      fontSize: "0.85rem",
                    }}
                    onClick={() => onEnroll && onEnroll(course.id)}
                  >
                    + Enroll Now
                  </button>
                )}
              </td>

              <td>
                <button
                  className="edit-btn"
                  onClick={() => onEdit(course)}
                >
                  Edit
                </button>

                <button
                  className="delete-btn"
                  onClick={() => onDelete(course.id)}
                >
                  Delete
                </button>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export default CourseTable;