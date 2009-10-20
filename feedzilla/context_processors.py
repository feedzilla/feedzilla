from django.conf import settings

from feedzilla import settings as app_settings

def feed(request):
    return {'FEEDZILLA_SITE_TITLE': app_settings.SITE_TITLE,
            'FEEDZILLA_SITE_DESCRIPTION': app_settings.SITE_DESCRIPTION,
            'FEEDZILLA_HEAD_LINKS': app_settings.HEAD_LINKS,
            }
