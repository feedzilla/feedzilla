from datetime import datetime

from django.conf import settings

FEEDZILLA_PAGE_SIZE = 25
FEEDZILLA_SUMMARY_SIZE = 2000
FEEDZILLA_SITE_TITLE = 'Yet another feedzilla site'
FEEDZILLA_SITE_DESCRIPTION = 'Edit your settings to change that line'
FEEDZILLA_HEAD_LINKS = ()
FEEDZILLA_COPYRIGHTS = '%d &copy; Feedzilla Aggregator' % datetime.now().year
FEEDZILLA_FEEDBURNER_FEED = None
FEEDZILLA_FEEDBURNER_COUNTER = False
