
from pydantic import BaseModel, Field


class LearningPathRequest(BaseModel):
    current_skills: list[str] = Field(..., description="List of skills the user currently possesses", example=["Java", "SQL"])
    career_goal: str = Field(..., description="Target career role or goal", example="Backend Developer")


class RecommendedCourse(BaseModel):
    title: str = Field(..., description="Course title")
    description: str = Field(..., description="Course summary or objective")
    category: str | None = Field(default="General", description="Course category")
    difficulty: str | None = Field(default="Beginner", description="Course difficulty level")
    reason: str = Field(..., description="Why this course is recommended for the career goal")


class RoadmapStep(BaseModel):
    week: int = Field(..., description="Week number or milestone index")
    topic: str = Field(..., description="Focus area or module topic")
    description: str = Field(..., description="Detailed instructions or tasks for this step")
    skills_to_acquire: list[str] = Field(default_factory=list, description="Skills targeted in this milestone")


class LearningPathResponse(BaseModel):
    career_goal: str = Field(..., description="The target career role")
    recommended_courses: list[RecommendedCourse] = Field(default_factory=list, description="Curated course recommendations")
    learning_path: list[RoadmapStep] = Field(default_factory=list, description="Weekly step-by-step roadmap")
    estimated_duration: str = Field(..., description="Total estimated time commitment (e.g., '8 Weeks')")
    difficulty: str = Field(..., description="Overall path difficulty (e.g., 'Beginner', 'Intermediate', 'Advanced')")
    summary: str = Field(..., description="Executive AI summary explaining the customized roadmap")


class AIChatRequest(BaseModel):
    message: str = Field(..., description="User message or prompt for the AI assistant", example="How do I prepare for a Senior Java Developer interview?")
    career_goal: str | None = Field(default=None, description="Optional current user career goal for context")
    current_skills: list[str] | None = Field(default=None, description="Optional user skills for context")


class AIChatResponse(BaseModel):
    response: str = Field(..., description="AI assistant response message")
    history_length: int = Field(..., description="Current count of messages in conversation history")
