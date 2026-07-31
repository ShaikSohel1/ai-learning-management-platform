from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_admin
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, UpdatePasswordRequest
from app.services.auth_service import login_user, register_user, update_user_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: RegisterRequest,
    db: Session = Depends(get_db)
):
    new_user = register_user(db, user)

    return {
        "message": "User registered successfully",
        "id": new_user.id,
        "email": new_user.email
    }


@router.post("/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):
    token = login_user(db, user)

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "department": current_user.department,
        "designation": current_user.designation
    }

@router.get("/admin")
def admin_dashboard(
    current_user: User = Depends(require_admin)
):
    return {
        "message": "Welcome Admin",
        "user": current_user.name
    }

@router.post("/update-password")
def update_password(
    data: UpdatePasswordRequest,
    db: Session = Depends(get_db)
):
    update_user_password(db, data.email, data.new_password)
    return {
        "success": True,
        "message": "Password updated successfully"
    }