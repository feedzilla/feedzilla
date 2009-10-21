import logging
import os.path
from datetime import datetime

from django.core.management.base import BaseCommand

from feedzilla.models import Feed

class Command(BaseCommand):
    help = u'Show the statistics about feed.'

    def handle(self, *args, **kwargs):
        logging.basicConfig(level=logging.DEBUG)

        query = args[0]

        feeds = Feed.objects.filter(site_url__icontains=query)
        for feed in feeds:

            line =  'Feed: %s' % feed.site_url
            border = '=' * len(line)
            print '%s\n%s\n%s' % (border, line, border)

            for post in feed.posts.order_by('-created')[:10]:
                status = 'YES' if post.active else 'NO'
                print '%s: %s' % (post.title.encode('utf-8'), status)
                print '  %s' % post.link
