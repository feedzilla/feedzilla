from django.conf import settings

from feedzilla import settings as app_settings

def feed(request):
    return {'SITE_TITLE': app_settings.SITE_TITLE,
            'SITE_DESCRIPTION': app_settings.SITE_DESCRIPTION,
            }
