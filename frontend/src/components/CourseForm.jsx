import { useEffect, useState } from "react";

const initialState = {
  title: "",
  description: "",
  category: "",
  duration: "",
  difficulty: "",
};

function CourseForm({
  editingCourse,
  onCreate,
  onUpdate,
}) {
  const [formData, setFormData] = useState(initialState);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (editingCourse) {
      setFormData({
        title: editingCourse.title,
        description: editingCourse.description,
        category: editingCourse.category,
        duration: editingCourse.duration,
        difficulty: editingCourse.difficulty,
      });
    } else {
      setFormData(initialState);
    }

    setErrors({});
  }, [editingCourse]);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    setErrors((prev) => ({
      ...prev,
      [name]: "",
    }));
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.title.trim()) {
      newErrors.title = "Course title is required.";
    } else if (formData.title.trim().length < 3) {
      newErrors.title = "Title must be at least 3 characters.";
    }

    if (!formData.description.trim()) {
      newErrors.description = "Description is required.";
    } else if (formData.description.trim().length < 10) {
      newErrors.description =
        "Description must be at least 10 characters.";
    }

    if (!formData.category.trim()) {
      newErrors.category = "Category is required.";
    }

    if (!formData.duration) {
      newErrors.duration = "Duration is required.";
    } else if (Number(formData.duration) <= 0) {
      newErrors.duration =
        "Duration must be greater than 0.";
    }

    if (!formData.difficulty) {
      newErrors.difficulty =
        "Please select a difficulty level.";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    const payload = {
      ...formData,
      title: formData.title.trim(),
      description: formData.description.trim(),
      category: formData.category.trim(),
      duration: Number(formData.duration),
    };

    if (editingCourse) {
      onUpdate(payload);
    } else {
      onCreate(payload);
    }

    setFormData(initialState);
    setErrors({});
  };

  return (
    <div className="course-form-container">
      <h3>
        {editingCourse
          ? "Edit Course"
          : "Add New Course"}
      </h3>

      <form
        className="course-form"
        onSubmit={handleSubmit}
      >
        <div>
          <input
            type="text"
            name="title"
            placeholder="Course Title"
            value={formData.title}
            onChange={handleChange}
          />
          {errors.title && (
            <small className="form-error">
              {errors.title}
            </small>
          )}
        </div>

        <div>
          <textarea
            name="description"
            placeholder="Description"
            value={formData.description}
            onChange={handleChange}
          />
          {errors.description && (
            <small className="form-error">
              {errors.description}
            </small>
          )}
        </div>

        <div>
          <input
            type="text"
            name="category"
            placeholder="Category"
            value={formData.category}
            onChange={handleChange}
          />
          {errors.category && (
            <small className="form-error">
              {errors.category}
            </small>
          )}
        </div>

        <div>
          <input
            type="number"
            name="duration"
            placeholder="Duration (Hours)"
            value={formData.duration}
            onChange={handleChange}
          />
          {errors.duration && (
            <small className="form-error">
              {errors.duration}
            </small>
          )}
        </div>

        <div>
          <select
            name="difficulty"
            value={formData.difficulty}
            onChange={handleChange}
          >
            <option value="">
              Select Difficulty
            </option>

            <option value="Beginner">
              Beginner
            </option>

            <option value="Intermediate">
              Intermediate
            </option>

            <option value="Advanced">
              Advanced
            </option>
          </select>

          {errors.difficulty && (
            <small className="form-error">
              {errors.difficulty}
            </small>
          )}
        </div>

        <button type="submit">
          {editingCourse
            ? "Update Course"
            : "Add Course"}
        </button>
      </form>
    </div>
  );
}

export default CourseForm;