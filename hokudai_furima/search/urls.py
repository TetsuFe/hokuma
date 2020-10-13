from django.conf.urls import url
from . import views

app_name = "search"

urlpatterns = [
        url(r'^product/$', views.search_product, name='search_product'),
        url(r'^product/ajax/$', views.search_product_ajax, name='search_product_ajax'),
        #url(r'^details/(?P<pk>.+)/$', views.product_details, name='product_details'),
    ]
