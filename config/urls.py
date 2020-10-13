from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path


urlpatterns = [
    url(r'account/', include('hokudai_furima.account.urls')),
    url(r'product/', include('hokudai_furima.product.urls')),
    url(r'search/', include('hokudai_furima.search.urls')),
    url(r'chat/', include('hokudai_furima.chat.urls')),
    url(r'todo_list/', include('hokudai_furima.todo_list.urls')),
    url(r'contact/', include('hokudai_furima.contact.urls')),
    url(r'^', include('hokudai_furima.core.urls')),
    url(r'rating/', include('hokudai_furima.rating.urls')),
    url(r'notification/', include('hokudai_furima.notification.urls')),
    url(r'guide/', include('hokudai_furima.guide.urls')),
    url(r'watchlist/', include('hokudai_furima.watchlist.urls')),
    url(r'offer/', include('hokudai_furima.matching_offer.urls')),
    url(r'rules/', include('hokudai_furima.site_rules.urls')),
    path('lecture/', include('hokudai_furima.lecture.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 画像への直リンクを使う場合は必要。この一行がなくても、{{user.icon.url}}で表示することは可能

if settings.DEBUG:
    urlpatterns += path('admin/', admin.site.urls),

    # for debug_toolbar
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
