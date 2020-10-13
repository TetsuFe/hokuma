from django.db import models
from django.conf import settings
from hokudai_furima.product.models import Product
from django.utils import timezone

class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    is_done = models.BooleanField(default=False)
    message = models.TextField(max_length=256, null=True) 
    relative_url = models.TextField(max_length=256, null=True) 
    created_date = models.DateTimeField(default=timezone.now)

    def done(self):
        self.is_done = True

    def update(self):
        self.save()

class ReportToRecieveTodo(Todo):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def set_template_message(self):
        self.message = '「'+self.product.title+'」の受け取りが完了しましたら、「商品を受け取りました」をクリックしてください'


class RatingTodo(Todo):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def set_template_message(self):
        if self.user == self.product.seller:
            self.message = self.product.buyer.username+'との間での「'+self.product.title+'」の受け渡しの完了を確認しました。最後に購入者を評価してください。'
        else:
            self.message = self.product.seller.username+'との間での「'+self.product.title+'」の受け渡しの完了を確認しました。最後に出品者を評価してください。'
