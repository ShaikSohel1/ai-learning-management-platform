from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    course_id = Column(Integer, ForeignKey("courses.id"))

    progress = Column(Integer)

    status = Column(String(50))

    enrolled_at = Column(Date)

    user = relationship("User", back_populates="enrollments")

    course = relationship("Course", back_populates="enrollments")