from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.auth import RegisterRequest


def register_user(db: Session, user: RegisterRequest):
    statement = select(User).where(User.email == user.email)
    existing_user = db.scalar(statement)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

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
    statement = select(User).where(User.email == user.email)
    db_user = db.scalar(statement)
    
    if db_user is None:
        return None

    if not verify_password(user.password, db_user.password):
        return None

    token = create_access_token({"sub": str(db_user.id)})
    return token


def update_user_password(db: Session, email: str, new_password: str):
    if len(new_password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long"
        )
    
    statement = select(User).where(User.email == email)
    db_user = db.scalar(statement)

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User account not found"
        )

    db_user.password = hash_password(new_password)
    db.commit()
    db.refresh(db_user)
    return db_user

