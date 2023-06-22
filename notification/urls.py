from django.urls import path
from . import views

urlpatterns = [
    path("notification/", views.notification, name="notification"),
    path("mark_notification_read/<int:notification_id>", views.mark_notification_read, name="mark_notification_read")
]