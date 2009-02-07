from django.conf.urls.defaults import *
from feed.syndication import PostFeed

feed_dict = {
    'posts': PostFeed,
}

urlpatterns = patterns('feed.views',
    url(r'^$', 'index', name='index'),
    url('^post/(?P<post_id>\d+)/$', 'post', name='feedzilla_post'),
    url('^feed/(?P<feed_id>\d+)/$', 'feed'),
    url('^tag/(?P<tag_value>.+)/$', 'tag', name='feedzilla_tag'),
    url('^sources/$', 'sources'),
    url('^search/$', 'search', name='search'),
)

urlpatterns += patterns('django.contrib.syndication.views',
    url(r'^feeds/(?P<url>.*)/$', 'feed', {'feed_dict': feed_dict}, name='feedzilla_feed'),
)
