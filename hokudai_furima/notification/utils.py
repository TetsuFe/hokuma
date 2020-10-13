from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def fetch_notification_list(request):
    notification_list = Notification.objects.filter(reciever=request.user).order_by('-created_date')
    for notification in notification_list:
        if notification.unread:
            notification.unread = False
            notification.save()
            notification.unread = True
    return notification_list
