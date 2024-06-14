from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from users.authentication import jwt_auth
from .models import Notification
from .schemas import NotificationSchema

notifications_router = Router(tags=["Notifications"])


@notifications_router.get("/", auth=jwt_auth, response={200: List[NotificationSchema], 403: dict})
def list_notifications(request):
    notifications = Notification.objects.filter(user=request.auth, is_read=False)
    return notifications


@notifications_router.post("/{notification_id}/read", auth=jwt_auth, response={200: dict, 404: dict})
def mark_as_read(request, notification_id: int):
    notification = get_object_or_404(Notification, id=notification_id, user=request.auth)
    notification.is_read = True
    notification.save()
    return {"success": True}
