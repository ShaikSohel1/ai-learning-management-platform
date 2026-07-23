from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class EmployeeSkill(Base):
    __tablename__ = "employee_skills"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    skill_id = Column(Integer, ForeignKey("skills.id"))

    proficiency = Column(String(50))

    last_updated = Column(DateTime)

    user = relationship("User", back_populates="employee_skills")

    skill = relationship("Skill", back_populates="employee_skills")