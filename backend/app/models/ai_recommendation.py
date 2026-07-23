from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    course_id = Column(Integer, ForeignKey("courses.id"))

    recommendation_reason = Column(String)

    generated_at = Column(DateTime)

    user = relationship("User", back_populates="ai_recommendations")

    course = relationship("Course", back_populates="ai_recommendations")