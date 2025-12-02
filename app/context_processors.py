from django.conf import settings

def site_settings(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DOMAIN': settings.SITE_DOMAIN,
        'DEBUG': settings.DEBUG,
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'TIME_ZONE': settings.TIME_ZONE,
    }