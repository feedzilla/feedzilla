# -*- coding: utf-8 -*-
import logging
from datetime import datetime
import re

from django.core.management.base import BaseCommand
from django.conf import settings

from feedzilla.util.parse import parse_feed
from feedzilla.models import Feed, Post
from feedzilla import settings

REX_TAGS_TAIL = re.compile(',[^,]*')

class Command(BaseCommand):
    help = u'Update feeds'

    def handle(self, *args, **kwargs):
        logging.basicConfig(level=logging.DEBUG)

        processors = []
        for path in settings.FEEDZILLA_POST_PROCESSORS:
            module_path, cls = path.rsplit('.', 1)
            module = __import__(module_path, globals(), locals(), ['foo'])
            proc = getattr(module, cls)()
            processors.append(proc)

        for feed in Feed.objects.filter(active=True):
            logging.debug('parsing %s' % feed.feed_url)

            resp = parse_feed(feed.feed_url, etag=feed.etag,
                              summary_size=settings.FEEDZILLA_SUMMARY_SIZE)
            if not resp['success']:
                logging.debug('Failure')
            else:
                new_posts = 0
                for entry in resp['entries']:
                    try:
                        Post.objects.get(guid=entry['guid'])
                    except Post.DoesNotExist:
                        tags = entry['tags']
                        if settings.FEEDZILLA_TAGS_LOWERCASE:
                            tags = set(x.lower() for x in tags)

                        # Strip tags to 255 chars string
                        # because of TagField limitation
                        tags = ', '.join(tags)
                        tags = REX_TAGS_TAIL.sub('', tags)[:255]

                        post = Post(
                            feed=feed,
                            tags=', '.join(tags),
                            title=entry['title'],
                            content=entry['content'],
                            summary=entry['summary'],
                            link=entry['link'],
                            guid=entry['guid'],
                            created=entry['created']
                        )
                        post.save()

                        # Remember post details
                        post_snapshot = post.__dict__

                        for proc in processors:
                            proc.process(post)

                        # If post was changed by some processor
                        # then save changes
                        if post.__dict__ != post_snapshot:
                            post.save()

                        new_posts += 1
                logging.debug('New posts: %d' % new_posts)

            feed.last_checked = datetime.now()
            feed.save()
            feed.update_counts()
