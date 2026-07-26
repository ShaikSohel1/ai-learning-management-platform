from datetime import datetime, UTC
import uuid
import logging
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.certificate import Certificate
from app.models.user import User

logger = logging.getLogger(__name__)


def enroll_user(db: Session, user_id: int, course_id: int) -> Enrollment:
    """
    Enrolls a user into a course. Prevents duplicate enrollments.
    Sets initial status to NOT_STARTED.
    """
    # Verify course exists
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found."
        )

    # Check duplicate enrollment
    existing = (
        db.query(Enrollment)
        .filter(Enrollment.user_id == user_id, Enrollment.course_id == course_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already enrolled in this course."
        )

    now = datetime.now(UTC)
    new_enrollment = Enrollment(
        user_id=user_id,
        course_id=course_id,
        status="NOT_STARTED",
        progress_percentage=0,
        started_at=now,
        created_at=now,
        updated_at=now,
        certificate_generated=False
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    logger.info(f"User ID {user_id} successfully enrolled in Course ID {course_id}")
    return new_enrollment


def get_user_enrollments(db: Session, user_id: int) -> List[Enrollment]:
    """
    Fetches all course enrollments for the specified user with course & certificate details.
    """
    return (
        db.query(Enrollment)
        .options(joinedload(Enrollment.course))
        .filter(Enrollment.user_id == user_id)
        .order_by(Enrollment.id.desc())
        .all()
    )


def get_enrollment_by_id(db: Session, enrollment_id: int, user_id: int) -> Enrollment:
    """
    Fetches details for a specific enrollment belonging to the authenticated user.
    """
    enrollment = (
        db.query(Enrollment)
        .options(joinedload(Enrollment.course))
        .filter(Enrollment.id == enrollment_id, Enrollment.user_id == user_id)
        .first()
    )
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment record not found."
        )
    return enrollment


def update_enrollment_progress(
    db: Session,
    enrollment_id: int,
    user_id: int,
    progress_percentage: int
) -> Enrollment:
    """
    Updates progress percentage and executes automated status transition state machine:
    - progress > 0 & status == 'NOT_STARTED' -> status = 'IN_PROGRESS'
    - progress == 100 -> status = 'COMPLETED', completed_at = now(), auto-generate certificate.
    """
    enrollment = get_enrollment_by_id(db, enrollment_id, user_id)
    now = datetime.now(UTC)

    enrollment.progress_percentage = progress_percentage
    enrollment.updated_at = now

    # Automated Workflow Transitions
    if progress_percentage > 0 and enrollment.status == "NOT_STARTED":
        enrollment.status = "IN_PROGRESS"
        logger.info(f"Enrollment ID {enrollment_id} status auto-updated to IN_PROGRESS")

    if progress_percentage >= 100:
        enrollment.progress_percentage = 100
        enrollment.status = "COMPLETED"
        if not enrollment.completed_at:
            enrollment.completed_at = now
        
        # Auto-generate Certificate if not already generated
        if not enrollment.certificate_generated:
            generate_certificate_internal(db, user_id=user_id, course_id=enrollment.course_id, enrollment=enrollment)

    db.commit()
    db.refresh(enrollment)
    return enrollment


def complete_enrollment(db: Session, enrollment_id: int, user_id: int) -> Enrollment:
    """
    Marks enrollment as 100% completed and triggers certificate generation.
    """
    return update_enrollment_progress(
        db=db,
        enrollment_id=enrollment_id,
        user_id=user_id,
        progress_percentage=100
    )


def generate_certificate_internal(
    db: Session,
    user_id: int,
    course_id: int,
    enrollment: Enrollment
) -> Certificate:
    """
    Internal helper function generating a unique Certificate record.
    """
    existing_cert = (
        db.query(Certificate)
        .filter(Certificate.user_id == user_id, Certificate.course_id == course_id)
        .first()
    )
    if existing_cert:
        enrollment.certificate_generated = True
        return existing_cert

    cert_number = f"CERT-{user_id}-{course_id}-{uuid.uuid4().hex[:6].upper()}"
    now = datetime.now(UTC)

    certificate = Certificate(
        user_id=user_id,
        course_id=course_id,
        certificate_number=cert_number,
        issued_at=now,
        certificate_url=f"/certificates/{cert_number}"
    )

    db.add(certificate)
    enrollment.certificate_generated = True
    logger.info(f"Generated Certificate {cert_number} for User ID {user_id}, Course ID {course_id}")
    return certificate


def get_certificate_for_enrollment(db: Session, enrollment_id: int, user_id: int) -> Optional[Certificate]:
    """
    Fetches the issued certificate for a specific completed enrollment.
    """
    enrollment = get_enrollment_by_id(db, enrollment_id, user_id)
    if enrollment.status != "COMPLETED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certificate is only available for completed courses."
        )

    cert = (
        db.query(Certificate)
        .filter(Certificate.user_id == user_id, Certificate.course_id == enrollment.course_id)
        .first()
    )
    if not cert:
        # Generate on the fly if missing
        cert = generate_certificate_internal(db, user_id, enrollment.course_id, enrollment)
        db.commit()
        db.refresh(cert)

    return cert


def delete_enrollment(db: Session, enrollment_id: int, user_id: int) -> bool:
    """
    Removes user's course enrollment.
    """
    enrollment = get_enrollment_by_id(db, enrollment_id, user_id)
    db.delete(enrollment)
    db.commit()
    logger.info(f"Enrollment ID {enrollment_id} deleted by User ID {user_id}")
    return True
