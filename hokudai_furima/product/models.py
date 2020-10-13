from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models import F, Max, Q
from versatileimagefield.fields import PPOIField, VersatileImageField
import os
from versatileimagefield.placeholder import OnDiscPlaceholderImage
from django.core.exceptions import ValidationError
from enum import Enum
from hokudai_furima.watchlist.models import WatchList
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from hokudai_furima.lecture.models import LectureCategory


class AccessLevelChoice(Enum):   # A subclass of Enum
    public = "公開"
    private = "非公開"

def has_no_singlequote(value):
    if "\'" in value:
        raise ValidationError(
            '商品名にはシングルクオート（\'）を含めないでください。',
            params={'value': value},
        )


class Category(MPTTModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.CASCADE)
    background_image = VersatileImageField(
        upload_to='category-backgrounds', blank=True, null=True)

    objects = models.Manager()
    tree = TreeManager()

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller')
    title  = models.CharField('商品名', max_length=200, validators=[has_no_singlequote])
    description = models.TextField('説明文', max_length=2000)
    price = models.PositiveIntegerField('値段(円)', default=0)
    is_sold = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    sold_date = models.DateTimeField(blank=True, null=True)
    wanting_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='wanting_users', blank=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='buyer')
    access_level = models.CharField('公開/非公開',
        max_length=10,
        choices=[(level.name, level.value) for level in AccessLevelChoice],
        default='public'
    )
    watched_count = models.PositiveIntegerField(default=0)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, blank=True, null=True, default=None)
    category = models.ForeignKey(
        Category, related_name='product_category_products', on_delete=models.PROTECT, blank=True, null=True)
    lecture_category = models.ForeignKey(
        LectureCategory, related_name='lecture_category_products', on_delete=models.PROTECT, blank=True, null=True)

    def update(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def increment_watched_count(self):
        self.watched_count += 1
        self.update()


class ProductImage(models.Model):
    image = VersatileImageField(
        '',
        upload_to='product', 
        blank=True,
        null=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def update(self):
        self.save()

    @property
    def thumbnail_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.thumbnail['600x600'].url

    @property
    def thumbnail_100_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.thumbnail['100x100'].url
