from django.conf.urls import url
from . import views

app_name = "contact"

urlpatterns = [
    url(r'^$', views.post_contact, name='post_contact'),
    url(r'^success/(?P<pk>\d+)/$', views.post_success, name='post_success'),
]
