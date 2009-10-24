# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from django.core.management.base import BaseCommand

from feedzilla.util.parse import parse_feed
from feedzilla.models import Feed, Post
from feedzilla import settings

class Command(BaseCommand):
    help = u'Update feeds'

    def handle(self, *args, **kwargs):
        logging.basicConfig(level=logging.DEBUG)

        for feed in Feed.objects.filter(active=True):
            logging.debug('parsing %s' % feed.feed_url)

            resp = parse_feed(feed.feed_url, etag=feed.etag,
                              summary_size=settings.SUMMARY_SIZE)
            if not resp['success']:
                logging.debug('Failure')
            else:
                new_posts = 0
                for entry in resp['entries']:
                    try:
                        Post.objects.get(guid=entry['guid'])
                    except Post.DoesNotExist:
                        post = Post(
                            feed=feed,
                            tags=', '.join(entry['tags']),
                            title=entry['title'],
                            content=entry['content'],
                            summary=entry['summary'],
                            link=entry['link'],
                            guid=entry['guid'],
                            created=entry['created']
                        )
                        post.save()
                        new_posts += 1
                logging.debug('New posts: %d' % new_posts)

            feed.last_checked = datetime.now()
            feed.save()
