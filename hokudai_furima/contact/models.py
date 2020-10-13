from django.db import models
from django.utils import timezone


class Contact(models.Model):
    text = models.TextField(('お問い合わせ内容'), max_length=1000)
    email = models.EmailField(('メールアドレス'), default='')
    created_date = models.DateTimeField(default=timezone.now)
