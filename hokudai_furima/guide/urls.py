from django.conf.urls import url
from . import views

app_name = "guide"

urlpatterns = [
    url(r'^sell$', views.sell_guide, name='sell_guide'),
    url(r'^buy$', views.buy_guide, name='buy_guide'),
]
