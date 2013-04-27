from django.conf import settings

def feedzilla_settings(request):
    result = {}
    for key in dir(settings):
        print 'key', key
        if key.startswith('FEEDZILLA_'):
            result[key] = getattr(settings, key)
    print result
    return result
