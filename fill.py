# -*- coding: utf-8
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

from feed.models import Feed

feed_list = [
    (u'веб мозги', 'http://web-brains.com/feeds/atom/blog/', 'http://web-brains.com/'),
]

Feed.objects.all().delete()
for title, feed_url, site_url in feed_list:
    feed = Feed.objects.create(title=title, feed_url=feed_url, site_url=site_url)
    feed.save()
