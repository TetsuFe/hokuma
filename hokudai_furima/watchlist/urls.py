from django.urls import path
from . import views

app_name = "watchlist"

urlpatterns = [
    path('', views.show_watch_list, name='show_watch_list'),
    path('add', views.add_watch_list, name='add_watch_list'),
    path('remove', views.remove_from_watch_list, name='remove_from_watch_list'),
    path('is_in_watch_list', views.is_in_watch_list, name='is_in_watch_list'),
]
