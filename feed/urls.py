from django.conf.urls.defaults import *

urlpatterns = patterns('feed.views',
    url(r'^$', 'index', name='index'),
    url('^post/(?P<post_id>\d+)/$', 'post', name='feedzilla_post'),
    url('^feed/(?P<feed_id>\d+)/$', 'feed'),
    url('^tag/(?P<tag_value>.+)/$', 'tag', name='feedzilla_tag'),
    url('^sources/$', 'sources'),
    url('^search/$', 'search', name='search'),
)

