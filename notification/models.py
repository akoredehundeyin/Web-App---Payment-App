from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.message

    @staticmethod
    def send_notification(recipient, notification_text):
        notification = Notification.objects.create(recipient=recipient, message=notification_text)
        return notification
