from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from mptt.managers import TreeManager
from mptt.models import MPTTModel


def has_no_singlequote(value):
    if "\'" in value:
        raise ValidationError(
            '商品名にはシングルクオート（\'）を含めないでください。',
            params={'value': value},
        )


class LectureCategory(MPTTModel):
    name = models.CharField('講義名', max_length=200, validators=[has_no_singlequote])
    description = models.TextField('説明文', max_length=2000)
    objects = models.Manager()
    tree = TreeManager()
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def update(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name
