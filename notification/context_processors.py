from .models import Notification


def pending_notifications(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient=request.user, read=False).count()
    else:
        count = 0
    return {"pending_notifications": count}