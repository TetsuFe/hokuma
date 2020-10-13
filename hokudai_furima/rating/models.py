from django.db import models
from django.utils import timezone
from django.conf import settings
from hokudai_furima.product.models import Product

class UserRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    rating_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rating_user')
    rated_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rated_user')
    rating = models.CharField(max_length=6)
