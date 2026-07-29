
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.enrollment import (
    CertificateResponse,
    EnrollmentCreate,
    EnrollmentResponse,
    ProgressUpdate,
)
from app.services import enrollment_service

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)


@router.get(
    "",
    response_model=list[EnrollmentResponse],
    summary="Get authenticated user's enrolled courses"
)
def get_my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return enrollment_service.get_user_enrollments(db=db, user_id=current_user.id)


@router.get(
    "/{enrollment_id}",
    response_model=EnrollmentResponse,
    summary="Get details of a specific enrollment"
)
def get_enrollment_details(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return enrollment_service.get_enrollment_by_id(
        db=db,
        enrollment_id=enrollment_id,
        user_id=current_user.id
    )


@router.post(
    "",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Enroll current user in a course"
)
def enroll_in_course(
    payload: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return enrollment_service.enroll_user(
        db=db,
        user_id=current_user.id,
        course_id=payload.course_id
    )


@router.put(
    "/{enrollment_id}/progress",
    response_model=EnrollmentResponse,
    summary="Update course progress percentage"
)
def update_progress(
    enrollment_id: int,
    payload: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return enrollment_service.update_enrollment_progress(
        db=db,
        enrollment_id=enrollment_id,
        user_id=current_user.id,
        progress_percentage=payload.progress_percentage
    )


@router.put(
    "/{enrollment_id}/complete",
    response_model=EnrollmentResponse,
    summary="Mark enrollment as 100% completed and issue certificate"
)
def mark_course_complete(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return enrollment_service.complete_enrollment(
        db=db,
        enrollment_id=enrollment_id,
        user_id=current_user.id
    )


@router.get(
    "/{enrollment_id}/certificate",
    response_model=CertificateResponse,
    summary="Get issued certificate for completed course"
)
def get_certificate(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cert = enrollment_service.get_certificate_for_enrollment(
        db=db,
        enrollment_id=enrollment_id,
        user_id=current_user.id
    )
    
    # Enrich with user and course names
    user_name = current_user.name
    course_title = cert.course.title if cert.course else "Course Completion"
    
    return CertificateResponse(
        id=cert.id,
        user_id=cert.user_id,
        course_id=cert.course_id,
        certificate_number=cert.certificate_number,
        user_name=user_name,
        course_title=course_title,
        issued_at=cert.issued_at,
        certificate_url=cert.certificate_url
    )


@router.delete(
    "/{enrollment_id}",
    summary="Remove a course enrollment"
)
def remove_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    enrollment_service.delete_enrollment(
        db=db,
        enrollment_id=enrollment_id,
        user_id=current_user.id
    )
    return {
        "message": "Enrollment removed successfully."
    }
