from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    course_id = Column(Integer, ForeignKey("courses.id"))

    certificate_url = Column(String)

    issued_at = Column(Date)

    expiry_date = Column(Date)

    user = relationship("User", back_populates="certificates")

    course = relationship("Course", back_populates="certificates")