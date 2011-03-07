from django.conf import settings

CONTEXT = {}
for key in dir(settings):
    if key.startswith('FEEDZILLA_'):
        CONTEXT[key] = getattr(settings, key)

def settings(request):
    return CONTEXT
