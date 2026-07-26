from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Notification(Base):
    """Notification SQLAlchemy Model."""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(String(1000), nullable=False)
    notification_type = Column(String(50), default="INFO")  # INFO, REMINDER, CERTIFICATE, RECOMMENDATION
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    user = relationship("User", backref="notifications")
