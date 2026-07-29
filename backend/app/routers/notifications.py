
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.services.notification_service import notification_service

router = APIRouter(
    prefix="/notifications",
    tags=["Notification Center"]
)


@router.get(
    "",
    response_model=list[NotificationResponse],
    summary="Get user notifications list"
)
def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notifs = notification_service.get_user_notifications(db=db, user_id=current_user.id)
    return [
        NotificationResponse(
            id=n.id,
            user_id=n.user_id,
            title=n.title,
            message=n.message,
            notification_type=n.notification_type,
            is_read=n.is_read,
            created_at=n.created_at.isoformat() if n.created_at else ""
        )
        for n in notifs
    ]


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create notification"
)
def create_notification(
    payload: NotificationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notif = notification_service.create_notification(
        db=db,
        user_id=current_user.id,
        title=payload.title,
        message=payload.message,
        notification_type=payload.notification_type or "INFO"
    )
    return NotificationResponse(
        id=notif.id,
        user_id=notif.user_id,
        title=notif.title,
        message=notif.message,
        notification_type=notif.notification_type,
        is_read=notif.is_read,
        created_at=notif.created_at.isoformat() if notif.created_at else ""
    )


@router.put(
    "/{notification_id}/read",
    summary="Mark notification as read"
)
def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = notification_service.mark_as_read(db=db, notification_id=notification_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found.")
    return {"success": True, "message": "Notification marked as read."}


@router.delete(
    "/{notification_id}",
    summary="Delete notification"
)
def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = notification_service.delete_notification(db=db, notification_id=notification_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found.")
    return {"success": True, "message": "Notification deleted."}
