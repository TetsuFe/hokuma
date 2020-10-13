from django.db import models
from hokudai_furima.account.models import User
from django.utils import timezone


class Notification(models.Model):
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    unread = models.BooleanField(default=True)
    message = models.TextField(max_length=256, null=True) 
    relative_url = models.TextField(max_length=256, null=True)
    created_date = models.DateTimeField(default=timezone.now)
