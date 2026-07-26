function CourseTable({ courses, onEdit, onDelete }) {
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
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        {courses.map((course) => (
          <tr key={course.id}>
            <td>{course.title}</td>

            <td>{course.category}</td>

            <td>{course.duration}</td>

            <td>{course.difficulty}</td>

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
        ))}
      </tbody>
    </table>
  );
}

export default CourseTable;