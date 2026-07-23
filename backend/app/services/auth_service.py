from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.core.security import hash_password


def register_user(db: Session, user: RegisterRequest):

    db_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role="User",
        department=user.department,
        designation=user.designation
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user