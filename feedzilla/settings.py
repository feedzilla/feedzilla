from django.conf import settings

def define(key, default):
    return getattr(settings, key, default)

PAGE_SIZE = define('FEEDZILLA_PAGE_SIZE', 25)
SUMMARY_SIZE = define('FEEDZILLA_SUMMARY_SIZE', 2000)
SITE_TITLE = define('FEEDZILLA_SITE_TITLE', 'Yet another feedzilla site')
SITE_DESCRIPTION = define('FEEDZILLA_SITE_DESCRIPTION', 'Edit your settings to change that line')
HEAD_LINKS = define('FEEDZILLA_HEAD_LINKS', ())
COPYRIGHTS = define('FEEDZILLA_COPYRIGHTS', ())
FEEDBURNER_FEED = define('FEEDZILLA_FEEDBURNER_FEED', None)
FEEDBURNER_COUNTER = define('FEEDZILLA_FEEDBURNER_COUNTER', False)
