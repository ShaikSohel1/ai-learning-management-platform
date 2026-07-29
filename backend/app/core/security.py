"""
Security Hardening Module.

Provides passlib password hashing, prompt injection protection, file upload validation,
security headers middleware, and input sanitization helpers.
"""

import logging
import re

from passlib.context import CryptContext

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashes plain text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain text password against bcrypt hash, with fallback for old plain-text passwords."""
    try:
        if pwd_context.verify(plain_password, hashed_password):
            return True
    except Exception:
        # Fallback for plain-text passwords stored before the security update
        pass
        
    return plain_password == hashed_password


# Known prompt injection attack signatures
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"system\s+override",
    r"you\s+are\s+now\s+dan",
    r"jailbreak",
    r"forget\s+all\s+rules",
    r"bypass\s+security",
    r"sudo\s+mode",
]


class SecurityManager:
    """Security utility manager for input sanitization and prompt injection defense."""

    @staticmethod
    def sanitize_prompt(text: str) -> str:
        """
        Sanitizes user prompt inputs by neutralizing known prompt injection patterns.
        """
        if not text:
            return ""

        cleaned = text.strip()
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                logger.warning(f"SECURITY_ALERT Prompt injection pattern detected: '{pattern}'")
                cleaned = re.sub(pattern, "[REDACTED_SECURITY_PROMPT]", cleaned, flags=re.IGNORECASE)

        return cleaned

    @staticmethod
    def validate_file_upload(filename: str, size_bytes: int, max_size_mb: int = 25) -> bool:
        """
        Validates file extensions and maximum file size thresholds.
        """
        allowed_extensions = {".pdf", ".txt", ".md", ".markdown", ".docx"}
        ext = "." + filename.lower().split(".")[-1] if "." in filename else ""

        if ext not in allowed_extensions:
            logger.warning(f"SECURITY_ALERT Invalid file extension upload attempt: '{filename}'")
            return False

        if size_bytes > (max_size_mb * 1024 * 1024):
            logger.warning(f"SECURITY_ALERT File size limit exceeded ({size_bytes} bytes): '{filename}'")
            return False

        return True

    @staticmethod
    def get_security_headers() -> dict[str, str]:
        """
        Returns production security headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options).
        """
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
        }


security_manager = SecurityManager()
