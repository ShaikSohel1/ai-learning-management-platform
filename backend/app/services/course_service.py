from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


def create_course(
    db: Session,
    course: CourseCreate,
    user_id: int
):
    # Check if course title already exists
    existing_course = db.scalar(
        select(Course).where(Course.title == course.title)
    )

    if existing_course:
        raise HTTPException(
            status_code=400,
            detail="Course with this title already exists"
        )

    db_course = Course(
        title=course.title,
        description=course.description,
        category=course.category,
        duration=course.duration,
        difficulty=course.difficulty,
        created_by=user_id
    )

    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


def get_all_courses(
    db: Session,
    search: str | None = None,
    category: str | None = None,
    difficulty: str | None = None,
    sort: str = "id",
    page: int = 1,
    limit: int = 10,
):
    statement = select(Course)

    # Search
    if search:
        statement = statement.where(
            Course.title.ilike(f"%{search}%")
        )

    # Filter by Category
    if category:
        statement = statement.where(
            Course.category == category
        )

    # Filter by Difficulty
    if difficulty:
        statement = statement.where(
            Course.difficulty == difficulty
        )

    # Sorting
    if sort == "title":
        statement = statement.order_by(Course.title)

    elif sort == "duration":
        statement = statement.order_by(Course.duration)

    elif sort == "difficulty":
        statement = statement.order_by(Course.difficulty)

    else:
        statement = statement.order_by(Course.id)

    # Pagination Validation
    page = max(page, 1)
    limit = min(max(limit, 1), 100)

    offset = (page - 1) * limit

    statement = (
        statement
        .offset(offset)
        .limit(limit)
    )

    return db.scalars(statement).all()


def get_course_by_id(
    db: Session,
    course_id: int
):
    return db.get(Course, course_id)


def update_course(
    db: Session,
    course_id: int,
    course: CourseUpdate
):
    db_course = db.get(Course, course_id)

    if db_course is None:
        return None

    # Check duplicate title (excluding current course)
    duplicate_course = db.scalar(
        select(Course).where(
            Course.title == course.title,
            Course.id != course_id
        )
    )

    if duplicate_course:
        raise HTTPException(
            status_code=400,
            detail="Course title already exists"
        )

    db_course.title = course.title
    db_course.description = course.description
    db_course.category = course.category
    db_course.duration = course.duration
    db_course.difficulty = course.difficulty

    db.commit()
    db.refresh(db_course)

    return db_course


def delete_course(
    db: Session,
    course_id: int
):
    db_course = db.get(Course, course_id)

    if db_course is None:
        return None

    db.delete(db_course)
    db.commit()

    return db_course