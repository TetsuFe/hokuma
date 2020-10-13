from django.conf.urls import url
from . import views

app_name = "chat"

urlpatterns = [
        url(r'^post/$', views.post_talk, name='post_talk'),
        url(r'^detele/$', views.delete_talk, name='delete_talk'),
    ]
