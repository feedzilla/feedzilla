from django.conf import settings

def feed(request):
    return {'SITE_TITLE': settings.FEEDZILLA_SITE_TITLE,
            'SITE_DESCRIPTION': settings.FEEDZILLA_SITE_DESCRIPTION,
            }
