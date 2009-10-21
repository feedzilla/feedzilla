from django.conf import settings

from feedzilla import settings as app_settings

def feed(request):
    keys = ('SITE_TITLE', 'SITE_DESCRIPTION', 'HEAD_LINKS',
            'COPYRIGHTS', 'FEEDBURNER_FEED', 'FEEDBURNER_COUNTER')
    return dict(('FEEDZILLA_%s' % x, getattr(app_settings, x)) for x in keys)
