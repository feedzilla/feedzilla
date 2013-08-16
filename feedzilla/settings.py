# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
FEEDZILLA_PAGE_SIZE = 25
FEEDZILLA_SUMMARY_SIZE = 2000
FEEDZILLA_SITE_TITLE = 'Yet another feedzilla site'
FEEDZILLA_SITE_DESCRIPTION = 'Edit your settings to change that line'
FEEDZILLA_TAGS_LOWERCASE = True
FEEDZILLA_POST_PROCESSORS = (
    'feedzilla.processors.ContentFilterProcessor',
)
FEEDZILLA_EXPAND_FULL = False

TAGGIT_TAGCLOUD_MAX = 4
