# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD

# Work around to make it compatible with Django 1.6
try:
    from django.conf.urls import *
except ImportError: 
    from django.conf.urls.defaults import *

from feedzilla.syndication import PostFeed

urlpatterns = patterns('feedzilla.views',
    url(r'^$', 'index', name='feedzilla_index'),
    url('^tag/([^/]+)$', 'tag', name='feedzilla_tag'),
    url('^sources$', 'source_list', name='feedzilla_source_list'),
    url('^search$', 'search', name='feedzilla_search'),
    url('^submit$', 'submit_blog', name='feedzilla_submit_blog'),
    url('^cloud$', 'cloud_page', name='feedzilla_cloud_page'),
)

urlpatterns += patterns('django.contrib.syndication.views',
    # WTF???
    url(r'^ru/projects/feed$', PostFeed(), name='feedzilla_feed'),
    # depprecated
    url(r'^feeds/posts$', PostFeed(), name='feedzilla_feed'),
    # new
    url(r'^feed/post$', PostFeed(), name='feedzilla_feed'),
)
