from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.core.security import hash_password
from sqlalchemy import select
from app.core.jwt import create_access_token
from app.core.security import verify_password

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

def login_user(db: Session, user):

    statement = select(User).where(
        User.email == user.email
    )
    db_user = db.scalar(statement)
    
    if db_user is None:
        return None

    if not verify_password(
        user.password,
        db_user.password
    ):
        return None

    token = create_access_token(
        {
            "sub": str(db_user.id)
        }
    )

    return token
