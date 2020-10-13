from django.conf.urls import url
from . import views

app_name = "rating"

urlpatterns = [
        url(r'^post/(?P<product_pk>\d+)/$', views.post_rating, name='post_rating'),
    ]
