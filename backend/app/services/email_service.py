"""
Email Service Module.

Formulates transactional email notifications (Course Completion, Reminders, Certificates).
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class EmailService:
    """Modular email generator service."""

    def send_course_completion_email(
        self,
        to_email: str,
        user_name: str,
        course_title: str,
        certificate_number: str
    ) -> Dict[str, Any]:
        subject = f"🏆 Congratulations! You completed '{course_title}'"
        body = (
            f"Dear {user_name},\n\n"
            f"Congratulations on completing '{course_title}'!\n"
            f"Your digital certificate #{certificate_number} has been generated and is available in your account.\n\n"
            "Keep up the great learning momentum!\n\n"
            "Best regards,\nAI LMS Enterprise Team"
        )
        logger.info(f"Simulated email sent to '{to_email}': {subject}")
        return {"status": "SENT", "to": to_email, "subject": subject, "body": body}

    def send_learning_reminder_email(
        self,
        to_email: str,
        user_name: str,
        course_title: str
    ) -> Dict[str, Any]:
        subject = f"⏰ Reminder: Continue your course '{course_title}'"
        body = (
            f"Hello {user_name},\n\n"
            f"This is a quick friendly reminder to spend 20 minutes on '{course_title}' today.\n"
            "Consistent daily micro-learning accelerates skill acquisition by 3x.\n\n"
            "Best regards,\nAI LMS Assistant"
        )
        logger.info(f"Simulated email sent to '{to_email}': {subject}")
        return {"status": "SENT", "to": to_email, "subject": subject, "body": body}


email_service = EmailService()
