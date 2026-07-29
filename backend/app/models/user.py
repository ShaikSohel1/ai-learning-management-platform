from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    department = Column(String(100))
    designation = Column(String(100))
    created_at = Column(DateTime, default=lambda:datetime.now(UTC))

    # Relationships
    enrollments = relationship("Enrollment", back_populates="user")
    employee_skills = relationship("EmployeeSkill", back_populates="user")
    certificates = relationship("Certificate", back_populates="user")
    ai_recommendations = relationship("AIRecommendation", back_populates="user")
    created_courses = relationship("Course", back_populates="creator")