from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

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
    status: str | None = Field(None, description="Enrollment status: NOT_STARTED, IN_PROGRESS, COMPLETED")
    progress_percentage: int | None = Field(None, ge=0, le=100)


class CertificateResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    certificate_number: str
    user_name: str | None = None
    course_title: str | None = None
    issued_at: datetime
    certificate_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    status: str
    progress_percentage: int
    started_at: datetime | None = None
    completed_at: datetime | None = None
    certificate_generated: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
    course: CourseResponse | None = None
    certificate: CertificateResponse | None = None

    model_config = ConfigDict(from_attributes=True)
