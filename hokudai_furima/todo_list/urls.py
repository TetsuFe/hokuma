from django.conf.urls import url
from . import views

app_name = "todo_list"

urlpatterns = [
        url(r'^add/$', views.add_todo_list, name='add_todo_list'),
        url(r'^$', views.show_todo_list, name='show_todo_list'),
        url(r'^ajax/undone_number/$', views.get_undone_number_ajax, name='get_undone_number_ajax'),
        #url(r'^details/(?P<pk>.+)/$', views.product_details, name='product_details'),
    ]
