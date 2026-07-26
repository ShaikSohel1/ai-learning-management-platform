import api from "./api";

// Get all courses
export const getCourses = async ({
  search = "",
  category = "",
  difficulty = "",
  sort = "id",
  page = 1,
  limit = 10,
} = {}) => {
  try {
    const response = await api.get("/courses", {
      params: {
        search,
        category,
        difficulty,
        sort,
        page,
        limit,
      },
    });

    return response.data;
  } catch (error) {
    console.error("Failed to fetch courses:", error);
    throw error;
  }
};

// Get course by ID
export const getCourseById = async (courseId) => {
  try {
    const response = await api.get(`/courses/${courseId}`);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch course:", error);
    throw error;
  }
};

// Create Course
export const createCourse = async (courseData) => {
  try {
    const response = await api.post("/courses", courseData);
    return response.data;
  } catch (error) {
    console.error("Failed to create course:", error);
    throw error;
  }
};

// Update Course
export const updateCourse = async (courseId, courseData) => {
  try {
    const response = await api.put(
      `/courses/${courseId}`,
      courseData
    );

    return response.data;
  } catch (error) {
    console.error("Failed to update course:", error);
    throw error;
  }
};

// Delete Course
export const deleteCourse = async (courseId) => {
  try {
    const response = await api.delete(
      `/courses/${courseId}`
    );

    return response.data;
  } catch (error) {
    console.error("Failed to delete course:", error);
    throw error;
  }
};

export const courseService = {
  getCourses,
  createCourse,
  updateCourse,
  deleteCourse,
};

export default courseService;