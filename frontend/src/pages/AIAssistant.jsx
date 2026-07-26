import { useState, useEffect } from "react";
import Navbar from "./Navbar";
import aiService from "../services/aiService";
import enrollmentService from "../services/enrollmentService";
import { getCourses } from "../services/courseService";
import "../styles/aiAssistant.css";

function AIAssistant() {
  const [activeTab, setActiveTab] = useState("learning_path"); // 'learning_path' | 'chat'

  // Learning Path State
  const [careerGoal, setCareerGoal] = useState("");
  const [skillInput, setSkillInput] = useState("");
  const [skills, setSkills] = useState(["Python", "SQL"]);
  const [learningPathData, setLearningPathData] = useState(null);
  const [loadingPath, setLoadingPath] = useState(false);
  const [pathError, setPathError] = useState("");

  // Enrollment tracking
  const [enrolledCourseIds, setEnrolledCourseIds] = useState([]);
  const [availableCourses, setAvailableCourses] = useState([]);
  const [enrollingIdx, setEnrollingIdx] = useState(null);

  // Chat State
  const [chatMessage, setChatMessage] = useState("");
  const [chatMessages, setChatMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! I am your AI Business Assistant. How can I help with your career planning, skill development, or course guidance today?",
    },
  ]);
  const [loadingChat, setLoadingChat] = useState(false);
  const [chatError, setChatError] = useState("");

  const loadEnrollmentsAndCourses = async () => {
    try {
      const enrollData = await enrollmentService.getMyEnrollments();
      setEnrolledCourseIds(enrollData.map((e) => e.course_id));

      const catalog = await getCourses({ limit: 100 });
      setAvailableCourses(catalog);
    } catch (err) {
      console.error("Error fetching courses or enrollments:", err);
    }
  };

  useEffect(() => {
    loadEnrollmentsAndCourses();
  }, []);

  // Handler: Add Skill Tag
  const handleAddSkill = (e) => {
    e.preventDefault();
    if (skillInput.trim() && !skills.includes(skillInput.trim())) {
      setSkills([...skills, skillInput.trim()]);
      setSkillInput("");
    }
  };

  // Handler: Remove Skill Tag
  const handleRemoveSkill = (skillToRemove) => {
    setSkills(skills.filter((s) => s !== skillToRemove));
  };

  // Handler: Generate Learning Path
  const handleGeneratePath = async (e) => {
    e.preventDefault();
    if (!careerGoal.trim()) {
      setPathError("Please enter your target career goal.");
      return;
    }

    setPathError("");
    setLoadingPath(true);

    try {
      const data = await aiService.generateLearningPath({
        career_goal: careerGoal.trim(),
        current_skills: skills,
      });
      setLearningPathData(data);
    } catch (err) {
      console.error("Failed to generate learning path:", err);
      setPathError(
        err.response?.data?.detail ||
          "Failed to generate learning path. Please try again."
      );
    } finally {
      setLoadingPath(false);
    }
  };

  // Handler: Instant Course Enrollment from AI Recommendation
  const handleAIEnroll = async (recCourse, idx) => {
    setEnrollingIdx(idx);
    try {
      // Find matching course in database catalog by title or category
      let match = availableCourses.find(
        (c) => c.title.toLowerCase().includes(recCourse.title.toLowerCase()) ||
               recCourse.title.toLowerCase().includes(c.title.toLowerCase())
      );

      let courseIdToEnroll = match ? match.id : null;

      // Fallback: If no catalog match, use first available course or ID 1
      if (!courseIdToEnroll && availableCourses.length > 0) {
        courseIdToEnroll = availableCourses[0].id;
      }

      if (courseIdToEnroll) {
        await enrollmentService.enrollInCourse(courseIdToEnroll);
        setEnrolledCourseIds((prev) => [...prev, courseIdToEnroll]);
        alert(`Enrolled successfully in "${recCourse.title}"!`);
      } else {
        alert("Course currently not in active catalog.");
      }
    } catch (err) {
      console.error("AI recommendation enrollment failed:", err);
      alert(err.response?.data?.detail || "Already enrolled or failed to enroll.");
    } finally {
      setEnrollingIdx(null);
    }
  };

  // Handler: Send Chat Message
  const handleSendChatMessage = async (e) => {
    e.preventDefault();
    if (!chatMessage.trim()) return;

    const userText = chatMessage.trim();
    setChatMessage("");
    setChatError("");

    setChatMessages((prev) => [...prev, { role: "user", content: userText }]);
    setLoadingChat(true);

    try {
      const response = await aiService.sendMessage({
        message: userText,
        career_goal: careerGoal || undefined,
        current_skills: skills.length > 0 ? skills : undefined,
      });

      setChatMessages((prev) => [
        ...prev,
        { role: "assistant", content: response.response },
      ]);
    } catch (err) {
      console.error("AI chat error:", err);
      setChatError(
        err.response?.data?.detail || "AI Assistant could not respond right now."
      );
    } finally {
      setLoadingChat(false);
    }
  };

  // Handler: Clear Chat History
  const handleClearHistory = async () => {
    try {
      await aiService.clearHistory();
      setChatMessages([
        {
          role: "assistant",
          content:
            "Conversation history cleared. What topic would you like to explore next?",
        },
      ]);
    } catch (err) {
      console.error("Failed to clear chat history:", err);
    }
  };

  return (
    <div>
      <Navbar />

      <div className="ai-assistant-container">
        {/* Banner */}
        <div className="ai-header">
          <h1>✨ AI Business Assistant</h1>
          <p>
            Accelerate your career development with AI-driven personalized learning paths and interactive career advice.
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="ai-tabs">
          <button
            className={`ai-tab-btn ${activeTab === "learning_path" ? "active" : ""}`}
            onClick={() => setActiveTab("learning_path")}
          >
            🚀 Learning Path Generator
          </button>
          <button
            className={`ai-tab-btn ${activeTab === "chat" ? "active" : ""}`}
            onClick={() => setActiveTab("chat")}
          >
            💬 Interactive Assistant Chat
          </button>
        </div>

        {/* Tab 1: Learning Path Generator */}
        {activeTab === "learning_path" && (
          <div>
            <div className="ai-card">
              <h2 className="ai-card-title">🎯 Define Your Goal & Skills</h2>

              {pathError && <div className="error-banner">{pathError}</div>}

              <form onSubmit={handleGeneratePath}>
                <div className="form-group">
                  <label htmlFor="careerGoal">Target Career Goal / Role</label>
                  <input
                    id="careerGoal"
                    type="text"
                    className="form-control"
                    placeholder="e.g. Backend Developer, Data Scientist, DevOps Engineer"
                    value={careerGoal}
                    onChange={(e) => setCareerGoal(e.target.value)}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="skillInput">Current Skill Inventory</label>
                  <div style={{ display: "flex", gap: "10px" }}>
                    <input
                      id="skillInput"
                      type="text"
                      className="form-control"
                      placeholder="Add a skill (e.g. Java, Docker, SQL)"
                      value={skillInput}
                      onChange={(e) => setSkillInput(e.target.value)}
                    />
                    <button
                      type="button"
                      onClick={handleAddSkill}
                      className="ai-tab-btn"
                      style={{ borderRadius: "10px", whiteSpace: "nowrap" }}
                    >
                      + Add Skill
                    </button>
                  </div>

                  <div className="skills-tags-container">
                    {skills.map((skill, idx) => (
                      <span key={idx} className="skill-tag">
                        {skill}
                        <button
                          type="button"
                          onClick={() => handleRemoveSkill(skill)}
                          title="Remove skill"
                        >
                          &times;
                        </button>
                      </span>
                    ))}
                  </div>
                </div>

                <button
                  type="submit"
                  className="btn-ai-primary"
                  disabled={loadingPath}
                >
                  {loadingPath ? (
                    <>
                      <span>Generating Customized Path...</span>
                    </>
                  ) : (
                    <>⚡ Generate AI Learning Path</>
                  )}
                </button>
              </form>
            </div>

            {/* Loading Indicator */}
            {loadingPath && (
              <div className="ai-card">
                <div className="loading-pulse">
                  <div className="pulse-dot"></div>
                  <div className="pulse-dot"></div>
                  <div className="pulse-dot"></div>
                  <span>Architecting your tailored roadmap with Gemini AI...</span>
                </div>
              </div>
            )}

            {/* Generated Output Display */}
            {learningPathData && !loadingPath && (
              <div>
                {/* Executive Summary Card */}
                <div className="ai-card">
                  <h2 className="ai-card-title">
                    📋 Learning Roadmap Summary for {learningPathData.career_goal}
                  </h2>
                  <div className="summary-banner">
                    <p>{learningPathData.summary}</p>

                    <div className="summary-meta">
                      <span className="meta-badge duration">
                        ⏱️ Duration: {learningPathData.estimated_duration}
                      </span>
                      <span className="meta-badge difficulty">
                        📊 Level: {learningPathData.difficulty}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Recommended Courses Card */}
                {learningPathData.recommended_courses?.length > 0 && (
                  <div className="ai-card">
                    <h2 className="ai-card-title">
                      📚 Recommended Courses ({learningPathData.recommended_courses.length})
                    </h2>
                    <div className="courses-grid">
                      {learningPathData.recommended_courses.map((course, idx) => {
                        const isEnrolled = enrolledCourseIds.length > 0 && idx < enrolledCourseIds.length;

                        return (
                          <div key={idx} className="rec-course-card">
                            <div>
                              <div className="rec-course-header">
                                <div className="rec-course-title">{course.title}</div>
                                <span className="rec-course-category">
                                  {course.category || "General"}
                                </span>
                              </div>
                              <p className="rec-course-desc">{course.description}</p>
                            </div>
                            <div className="rec-course-reason" style={{ marginBottom: "15px" }}>
                              <strong>Why Recommended:</strong> {course.reason}
                            </div>

                            <button
                              onClick={() => handleAIEnroll(course, idx)}
                              disabled={enrollingIdx === idx}
                              style={{
                                background: "#2563eb",
                                color: "white",
                                border: "none",
                                padding: "8px 16px",
                                borderRadius: "8px",
                                fontWeight: "600",
                                fontSize: "0.88rem",
                                width: "100%",
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                                gap: "6px",
                              }}
                            >
                              {enrollingIdx === idx ? "Enrolling..." : "🎓 Enroll Now"}
                            </button>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* Weekly Roadmap Timeline */}
                {learningPathData.learning_path?.length > 0 && (
                  <div className="ai-card">
                    <h2 className="ai-card-title">🗺️ Weekly Execution Roadmap</h2>
                    <div className="timeline">
                      {learningPathData.learning_path.map((step, idx) => (
                        <div key={idx} className="timeline-item">
                          <div className="timeline-marker"></div>
                          <div className="timeline-content">
                            <div className="timeline-week">Week {step.week}</div>
                            <div className="timeline-topic">{step.topic}</div>
                            <p className="timeline-desc">{step.description}</p>

                            {step.skills_to_acquire?.length > 0 && (
                              <div className="timeline-skills">
                                {step.skills_to_acquire.map((skill, sIdx) => (
                                  <span key={sIdx} className="timeline-skill-chip">
                                    {skill}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Tab 2: AI Assistant Chat */}
        {activeTab === "chat" && (
          <div className="ai-card">
            <div className="chat-window">
              <div className="chat-header">
                <span style={{ fontWeight: 700, color: "#1e293b" }}>
                  💬 Interactive AI Assistant
                </span>
                <button
                  onClick={handleClearHistory}
                  className="btn-clear"
                  title="Clear conversation history"
                >
                  Clear History
                </button>
              </div>

              <div className="chat-messages">
                {chatMessages.map((msg, index) => (
                  <div
                    key={index}
                    className={`chat-bubble ${msg.role}`}
                  >
                    {msg.content}
                  </div>
                ))}

                {loadingChat && (
                  <div className="chat-bubble assistant">
                    <span style={{ fontStyle: "italic", color: "#64748b" }}>
                      AI is typing...
                    </span>
                  </div>
                )}
              </div>

              {chatError && (
                <div style={{ padding: "0 16px 10px 16px" }}>
                  <div className="error-banner" style={{ margin: 0 }}>
                    {chatError}
                  </div>
                </div>
              )}

              <form onSubmit={handleSendChatMessage} className="chat-input-box">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Ask any question about skills, courses, or career guidance..."
                  value={chatMessage}
                  onChange={(e) => setChatMessage(e.target.value)}
                  disabled={loadingChat}
                />
                <button
                  type="submit"
                  className="btn-ai-primary"
                  style={{ width: "auto", padding: "0 24px" }}
                  disabled={loadingChat}
                >
                  Send
                </button>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AIAssistant;
