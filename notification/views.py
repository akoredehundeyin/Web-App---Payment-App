from django.shortcuts import render, redirect
from .models import Notification


def notification(request):
    notifications = list(Notification.objects.filter(recipient=request.user, read=False).order_by("-created"))
    return render(request, "notification/notifications.html", {"notifications": notifications})


def mark_notification_read(request, notification_id):
    read_notification = Notification.objects.get(pk=notification_id)
    read_notification.read = True
    read_notification.save()
    return redirect("notification")
