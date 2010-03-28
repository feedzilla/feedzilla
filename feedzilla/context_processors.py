from django.conf import settings

CONTEXT = {}
for key in settings.get_all_members():
    if key.startswith('FEEDZILLA_'):
        CONTEXT[key] = getattr(settings, key)

def settings(request):
    return CONTEXT
