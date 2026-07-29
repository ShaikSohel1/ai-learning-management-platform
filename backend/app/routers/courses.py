from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_admin
from app.models.user import User
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from app.services.course_service import (
    create_course,
    delete_course,
    get_all_courses,
    get_course_by_id,
    update_course,
)

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.post(
    "",
    response_model=CourseResponse
)
def add_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return create_course(
        db=db,
        course=course,
        user_id=current_user.id
    )


@router.get(
    "",
    response_model=list[CourseResponse]
)
def read_courses(
    search: str | None = None,
    category: str |None = None,
    difficulty: str | None = None,
    sort: str = "id",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_courses(
        db=db,
        search=search,
        category=category,
        difficulty=difficulty,
        sort=sort,
        page=page,
        limit=limit
    )


@router.get(
    "/{course_id}",
    response_model=CourseResponse
)
def read_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = get_course_by_id(
        db=db,
        course_id=course_id
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


@router.put(
    "/{course_id}",
    response_model=CourseResponse
)
def edit_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    updated_course = update_course(
        db=db,
        course_id=course_id,
        course=course
    )

    if updated_course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return updated_course


@router.delete("/{course_id}")
def remove_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    deleted_course = delete_course(
        db=db,
        course_id=course_id
    )

    if deleted_course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return {
        "message": "Course deleted successfully"
    }