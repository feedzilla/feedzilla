# -*- coding: utf-8
import os
import sys
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

from feed.models import Feed, FilterWord

feed_list = [
    (u'веб мозги', 'http://web-brains.com/feeds/atom/blog/', 'http://web-brains.com/'),
    (u'rabchevsky.name', 'http://rabchevsky.name/rss.xml', 'http://rabchevsky.name/'),
    (u'shcherbak.net', 'http://shcherbak.net/feed', 'http://shcherbak.net'),
]

for word in ['rdf', u'sparql', 'semantic']:
    FilterWord.objects.create(value=word)

Feed.objects.all().delete()
for title, feed_url, site_url in feed_list:
    feed = Feed.objects.create(title=title, feed_url=feed_url, site_url=site_url)
    feed.save()
