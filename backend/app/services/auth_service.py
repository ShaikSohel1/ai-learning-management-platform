import hashlib
import logging
import re
import secrets
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.models.password_reset_token import PasswordResetToken
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.services.email_service import send_password_reset_email

logger = logging.getLogger("auth_service")


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


def request_password_reset(db: Session, email: str):
    """
    Generates a secure password reset token for the specified user email,
    stores a SHA256 hash in the database, and dispatches the reset email via Resend.
    Always returns a generic success message to prevent email enumeration.
    """
    generic_response = {
        "success": True,
        "message": "If an account exists, a password reset link has been sent."
    }

    statement = select(User).where(User.email == email)
    db_user = db.scalar(statement)

    if db_user is None:
        logger.info(f"[Password Reset Request] Email '{email}' not found. Returning generic success.")
        return generic_response

    # Rate Limiting: Check if a token was created for this user within the last 60 seconds
    now = datetime.now(UTC)
    recent_token_stmt = (
        select(PasswordResetToken)
        .where(
            PasswordResetToken.user_id == db_user.id,
            PasswordResetToken.created_at >= now - timedelta(seconds=60)
        )
    )
    recent_token = db.scalar(recent_token_stmt)
    if recent_token:
        logger.warning(f"[Password Reset Rate Limit] User ID {db_user.id} requested reset within 60s limit.")
        return generic_response

    # Invalidate/delete any old unused tokens for this user
    db.execute(
        delete(PasswordResetToken).where(
            PasswordResetToken.user_id == db_user.id,
            PasswordResetToken.used == False
        )
    )

    # Generate 64-character urlsafe plaintext token and SHA256 token hash
    plaintext_token = secrets.token_urlsafe(64)
    token_hash = hashlib.sha256(plaintext_token.encode("utf-8")).hexdigest()
    expires_at = now + timedelta(minutes=30)

    # Store token hash in database
    reset_record = PasswordResetToken(
        user_id=db_user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        used=False,
        created_at=now
    )
    db.add(reset_record)
    db.commit()

    # Dispatch email via Resend
    send_password_reset_email(to_email=db_user.email, user_name=db_user.name, reset_token=plaintext_token)
    logger.info(f"[Password Reset Request] Successfully generated token for User ID {db_user.id}.")

    return generic_response


def validate_reset_token_service(db: Session, plaintext_token: str) -> dict:
    """
    Validates a password reset token by comparing its SHA256 hash against database records.
    Returns status: ok, invalid, used, or expired.
    """
    if not plaintext_token:
        return {"valid": False, "reason": "invalid"}

    token_hash = hashlib.sha256(plaintext_token.encode("utf-8")).hexdigest()
    statement = select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash)
    reset_record = db.scalar(statement)

    if not reset_record:
        return {"valid": False, "reason": "invalid"}

    if reset_record.used:
        return {"valid": False, "reason": "used"}

    now = datetime.now(UTC)
    # Ensure datetime object has timezone for accurate comparison
    record_expires = reset_record.expires_at
    if record_expires.tzinfo is None:
        record_expires = record_expires.replace(tzinfo=UTC)

    if record_expires < now:
        return {"valid": False, "reason": "expired"}

    return {
        "valid": True,
        "reason": "ok",
        "email": reset_record.user.email
    }


def reset_password_with_token(db: Session, plaintext_token: str, password: str, confirm_password: str):
    """
    Validates reset token, checks password strength & equality,
    hashes the new password via bcrypt, updates users.password, and invalidates the token.
    """
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    # Validate Password Strength Requirements
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one number.")
    if not re.search(r"[^a-zA-Z0-9]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one special character.")

    validation = validate_reset_token_service(db, plaintext_token)
    if not validation["valid"]:
        reason = validation["reason"]
        if reason == "expired":
            raise HTTPException(status_code=400, detail="This reset link has expired. Please request a new one.")
        elif reason == "used":
            raise HTTPException(status_code=400, detail="This reset link has already been used.")
        else:
            raise HTTPException(status_code=400, detail="Invalid reset link.")

    token_hash = hashlib.sha256(plaintext_token.encode("utf-8")).hexdigest()
    statement = select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash)
    reset_record = db.scalar(statement)

    user = reset_record.user
    user.password = hash_password(password)
    reset_record.used = True

    # Delete all previous reset tokens for this user
    db.execute(
        delete(PasswordResetToken).where(PasswordResetToken.user_id == user.id)
    )

    db.commit()
    logger.info(f"[Password Reset Success] Password updated for User ID {user.id} ({user.email}).")

    return {
        "success": True,
        "message": "Password reset successfully. You can now log in with your new password."
    }


