from django.urls import path, re_path
from . import views

app_name = "matching_offer"

urlpatterns = [
    re_path(r'^(?P<pk>\d+)/$', views.matching_offer_details, name='matching_offer_details'),
    path('chat/create', views.create_offer_talk, name='create_offer_talk'),
    path('chat/delete', views.delete_offer_talk, name='delete_offer_talk'),
    path('create', views.create_matching_offer, name='create_matching_offer'),
    re_path(r'^update/(?P<matching_offer_pk>\d+)/$', views.update_matching_offer, name='update_matching_offer'),
    path('latest', views.show_latest_matching_offer_list, name='show_latest_matching_offer_list'),
]
