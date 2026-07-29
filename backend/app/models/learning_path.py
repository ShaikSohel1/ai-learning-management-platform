from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String)
    target_role = Column(String(100))
    courses = relationship("LearningPathCourse",back_populates="learning_path")