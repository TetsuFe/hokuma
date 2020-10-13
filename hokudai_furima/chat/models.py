from django.db import models
from django.utils import timezone
from django.conf import settings
from hokudai_furima.product.models import Product


class Chat(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True) 
    product_seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='product_seller') 
    product_wanting_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='product_wanting_user') 
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def update(self):
        self.updated_date = timezone.now()
        self.save()


class Talk(models.Model):
    talker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True)
    sentence = models.TextField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def update(self):
        self.updated_date = timezone.now()
        self.save()

