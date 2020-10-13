from django.conf.urls import url
from . import views

app_name = "notification"

urlpatterns = [
        url(r'^$',views.index, name='index'),
        url(r'^ajax/unread_number/$',views.get_unread_number_ajax, name='get_unread_number_ajax'),
    ]
