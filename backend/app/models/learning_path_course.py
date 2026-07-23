from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database.base import Base


class LearningPathCourse(Base):
    __tablename__ = "learning_path_courses"

    id = Column(Integer, primary_key=True)

    learning_path_id = Column(
        Integer,
        ForeignKey("learning_paths.id")
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id")
    )

    sequence_order = Column(Integer)

    learning_path = relationship(
        "LearningPath",
        back_populates="courses"
    )

    course = relationship(
        "Course",
        back_populates="learning_path_courses"
    )