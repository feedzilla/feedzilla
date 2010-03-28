from django.conf import settings

KEYS = ('FEEDZILLA_SITE_TITLE', 'FEEDZILLA_SITE_DESCRIPTION',
        'FEEDZILLA_HEAD_LINKS', 'FEEDZILLA_COPYRIGHTS',
        'FEEDZILLA_FEEDBURNER_FEED', 'FEEDZILLA_FEEDBURNER_COUNTER',
        'FEEDZILLA_TWITTER')
CONTEXT = dict((x, getattr(settings, x)) for x in KEYS)

def settings(request):
    return CONTEXT
