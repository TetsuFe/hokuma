from django.conf import settings


def google_analytics(request):
    """
    DEBUG=Falseの場合に、GoogleアナリティクスのTAG MANAGER を使用するフラグを返す
    """
    if not settings.DEBUG:
        return {
            'GOOGLE_ANALYTICS_TAG_MANAGER_FLAG': True,
        }
    else:
        return {'GOOGLE_ANALYTICS_TAG_MANAGER_FLAG': False}

