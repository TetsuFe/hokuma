from django.urls import path
from . import views

app_name = "lecture"

urlpatterns = [
    path('details/<int:pk>/', views.lecture_category_details, name='lecture_category_details'),
    path('list/', views.lecture_category_list, name='lecture_category_list'),
    path('list/<int:pk>/', views.lecture_category_list_with_pk, name='lecture_category_list_with_pk'),
]
