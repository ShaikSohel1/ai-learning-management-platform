from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String)
    category = Column(String(100))
    duration = Column(Integer)
    difficulty = Column(String(50))
    created_by = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="created_courses")
    lessons = relationship("Lesson", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    certificates = relationship("Certificate", back_populates="course")
    ai_recommendations = relationship("AIRecommendation", back_populates="course")
    learning_path_courses = relationship("LearningPathCourse", back_populates="course")

