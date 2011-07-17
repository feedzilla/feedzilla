# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
from django.conf.urls.defaults import *

from feedzilla.syndication import PostFeed

feed_dict = {
    'posts': PostFeed,
}

urlpatterns = patterns('feedzilla.views',
    url(r'^$', 'index', name='feedzilla_index'),
    url('^tag/(?P<tag_value>.+)$', 'tag', name='feedzilla_tag'),
    url('^sources$', 'source_list', name='feedzilla_source_list'),
    url('^search$', 'search', name='feedzilla_search'),
    url('^submit$', 'submit_blog', name='feedzilla_submit_blog'),
)

urlpatterns += patterns('django.contrib.syndication.views',
    url(r'^feeds/(?P<url>.*)$', 'feed', {'feed_dict': feed_dict}, name='feedzilla_feed'),
)
