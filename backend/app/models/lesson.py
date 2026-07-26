from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String(255))
    video_url = Column(String)
    document_url = Column(String)
    lesson_order = Column(Integer)
    course = relationship("Course", back_populates="lessons")