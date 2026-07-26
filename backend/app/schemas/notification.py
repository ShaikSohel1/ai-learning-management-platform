from typing import Optional
from pydantic import BaseModel, Field


class NotificationCreate(BaseModel):
    title: str = Field(..., min_length=2)
    message: str = Field(..., min_length=2)
    notification_type: Optional[str] = Field("INFO")


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: str

    class Config:
        from_attributes = True
