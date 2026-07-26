from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from app.schemas.course import CourseResponse


class EnrollmentCreate(BaseModel):
    course_id: int = Field(..., description="ID of the course to enroll in")


class ProgressUpdate(BaseModel):
    progress_percentage: int = Field(..., ge=0, le=100, description="Completion percentage from 0 to 100")

    @field_validator("progress_percentage")
    @classmethod
    def validate_progress(cls, v: int) -> int:
        if not (0 <= v <= 100):
            raise ValueError("Progress percentage must be between 0 and 100")
        return v


class EnrollmentUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Enrollment status: NOT_STARTED, IN_PROGRESS, COMPLETED")
    progress_percentage: Optional[int] = Field(None, ge=0, le=100)


class CertificateResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    certificate_number: str
    user_name: Optional[str] = None
    course_title: Optional[str] = None
    issued_at: datetime
    certificate_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    status: str
    progress_percentage: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    certificate_generated: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    course: Optional[CourseResponse] = None
    certificate: Optional[CertificateResponse] = None

    model_config = ConfigDict(from_attributes=True)
