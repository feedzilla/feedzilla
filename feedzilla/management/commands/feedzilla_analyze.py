"""
Script for searching invalid or obsolete feeds.
"""
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
from grab import Grab
import re
from urlparse import urlsplit

from django.core.management.base import BaseCommand

from feedzilla.models import Feed

REX_FEED_URL = re.compile(r'feed|rss|atom', re.I)

class Command(BaseCommand):
    help = u'Search for invalid and obsolete feeds'

    def handle(self, *args, **kwargs):
        g = Grab()

        for feed in Feed.objects.all():
            host = urlsplit(feed.site_url).hostname
            ok = True
            resp = g.go(feed.site_url)
            
            # Check that request to Feed.site_url is not redirect elsewhere
            if resp.url != feed.site_url:
                print 'Site %s redirects to %s' % (feed.site_url, resp.url)
                ok = False

            tree = g.tree
            tree.make_links_absolute(resp.url)

            # Search for `Feed.feed_url` in HTML source of the page
            # fetched from `Feed.site_url` URL.
            found = False
            candidates = set()
            for elem, attr, url, pos in tree.iterlinks():
                if REX_FEED_URL.search(url):
                    candidates.add(url)
                if url == feed.feed_url:
                    found = True
                    break
            
            # If `Feed.feed_url` was not found then
            # display found link which probably is correct variant of the `feed_url`.
            if not found:
                print 'Feed url %s not found on Site %s' % (feed.feed_url, host)
                print 'Candidates:'
                print '\n'.join(candidates)
                ok = False

            if not ok:
                print


    if __name__ == '__main__':
        main()
