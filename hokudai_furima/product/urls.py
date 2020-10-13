from django.conf.urls import url
from . import views

app_name = "product"

urlpatterns = [
        url(r'^create/$', views.create_product, name='create_product'),
        url(r'^update/(?P<product_pk>\d+)/$', views.update_product, name='update_product'),
        url(r'^details/(?P<pk>\d+)/$', views.product_details, name='product_details'),
        url(r'^want/(?P<pk>\d+)/$', views.want_product, name='want_product'),
        url(r'^want/cancel/(?P<pk>\d+)/$', views.cancel_want_product, name='cancel_want_product'),
        url(r'^chat/direct/(?P<product_pk>\d+)/(?P<wanting_user_pk>\d+)/$', views.product_direct_chat, name='product_direct_chat'),
        url(r'^decide/sell/(?P<product_pk>\d+)/(?P<wanting_user_pk>\d+)/$', views.decide_to_sell, name='decide_to_sell'),
        url(r'^(?P<product_pk>\d+)/complete/recieve/$', views.complete_to_recieve, name='complete_to_recieve'),
        url(r'^category/details/(?P<pk>\d+)/$', views.category_details, name='category_details'),
    ]
