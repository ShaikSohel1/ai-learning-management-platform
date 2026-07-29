"""
Notification Service Module.

Manages user in-app notifications in PostgreSQL database.
"""

from sqlalchemy.orm import Session

from app.models.notification import Notification


class NotificationService:
    """Service managing database-backed user notifications."""

    def create_notification(
        self,
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notification_type: str = "INFO"
    ) -> Notification:
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False
        )
        db.add(notif)
        db.commit()
        db.refresh(notif)
        return notif

    def get_user_notifications(self, db: Session, user_id: int) -> list[Notification]:
        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(20)
            .all()
        )

    def mark_as_read(self, db: Session, notification_id: int, user_id: int) -> bool:
        notif = (
            db.query(Notification)
            .filter(Notification.id == notification_id, Notification.user_id == user_id)
            .first()
        )
        if notif:
            notif.is_read = True
            db.commit()
            return True
        return False

    def delete_notification(self, db: Session, notification_id: int, user_id: int) -> bool:
        notif = (
            db.query(Notification)
            .filter(Notification.id == notification_id, Notification.user_id == user_id)
            .first()
        )
        if notif:
            db.delete(notif)
            db.commit()
            return True
        return False


notification_service = NotificationService()
