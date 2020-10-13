from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
        url(r'^signup/$',views.signup, name='signup'),
        url(r'^login/$',views.login, name='login'),
        url(r'^logout/$', views.logout, name='logout'),
        url(r'^mypage/$', views.mypage, name='mypage'),
        url(r'^edit/$', views.edit, name='edit'),
        url(r'^(?P<user_pk>\d+)/$', views.others_page, name='others_page'),
        url(r'^activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  # noqa
            views.activation, name='activation'),
        url(r'^password/reset/$', views.password_reset,
            name='reset-password'),
        url(r'^password/reset/done/$', auth_views.PasswordResetDoneView.as_view(
            template_name='account/password_reset_done.html'),
            name='reset-password-done'),
        url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  # noqa
            views.password_reset_confirm, name='reset-password-confirm'),
        url(r'password/reset/complete/$', auth_views.PasswordResetCompleteView.as_view(  # noqa
            template_name='account/password_reset_from_key_done.html'),
            name='reset-password-complete'),
        url(r'^delete/$', views.delete, name='delete'),
    ]
