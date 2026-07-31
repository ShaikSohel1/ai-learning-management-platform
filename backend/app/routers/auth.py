from collections import defaultdict
from datetime import UTC, datetime, timedelta
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_admin
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    UpdatePasswordRequest,
)
from app.services.auth_service import (
    login_user,
    register_user,
    request_password_reset,
    reset_password_with_token,
    update_user_password,
    validate_reset_token_service,
)

logger = logging.getLogger("auth_router")

# In-memory rate limiting store: { ip: [timestamp1, timestamp2, ...] }
_ip_reset_attempts: dict[str, list[datetime]] = defaultdict(list)


def _get_client_ip(request: Request) -> str:
    """Extracts client IP safely considering reverse proxies like Render/Vercel."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        parts = [p.strip() for p in forwarded.split(",") if p.strip()]
        if parts:
            return parts[0]
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def _check_ip_rate_limit(client_ip: str, limit: int = 5, window_seconds: int = 60) -> bool:
    """
    Returns True if IP is within limits, False if rate limit exceeded.
    Per-IP limit: max `limit` requests per `window_seconds`.
    """
    now = datetime.now(UTC)
    cutoff = now - timedelta(seconds=window_seconds)

    attempts = [t for t in _ip_reset_attempts[client_ip] if t >= cutoff]
    _ip_reset_attempts[client_ip] = attempts

    if len(attempts) >= limit:
        return False

    _ip_reset_attempts[client_ip].append(now)
    return True


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

@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Sends a password reset email if the account exists.
    Enforces per-IP and per-email rate limiting while returning generic 200 OK.
    """
    client_ip = _get_client_ip(request)
    if not _check_ip_rate_limit(client_ip):
        logger.warning(f"[Rate Limit Exceeded] Per-IP limit reached for IP '{client_ip}'.")
        return {
            "success": True,
            "message": "If an account exists, a password reset link has been sent."
        }

    return request_password_reset(db, data.email)

@router.get("/validate-reset-token")
def validate_reset_token(
    token: str = Query(..., description="Plaintext reset token"),
    db: Session = Depends(get_db)
):
    """
    Validates if the provided reset token is valid, unused, and unexpired.
    """
    return validate_reset_token_service(db, token)

@router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Resets the user's password if the reset token is valid and new passwords match policy.
    """
    return reset_password_with_token(
        db=db,
        plaintext_token=data.token,
        password=data.password,
        confirm_password=data.confirm_password
    )