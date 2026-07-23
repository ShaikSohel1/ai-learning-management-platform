from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)

    name = Column(String(100))

    category = Column(String(100))

    description = Column(String)

    employee_skills = relationship(
        "EmployeeSkill",
        back_populates="skill"
    )