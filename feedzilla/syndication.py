# -*- coding: utf-8 -*-
import os
from datetime import datetime

from django.contrib.syndication.feeds import FeedDoesNotExist
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.conf import settings

from feedzilla.models import Post
from feedzilla import settings as app_settings


class PostFeed(Feed):
    feed_type = Atom1Feed
    link = '/'
    title = app_settings.SITE_TITLE
    subtitle = app_settings.SITE_DESCRIPTION

    #def item_link(self, obj):
        #return obj.get_imdb_link()

    def item_guid(self, obj):
        return str(obj.guid)

    def items(self, obj):
        return Post.active_objects.all()\
                   .order_by('-created')[:app_settings.PAGE_SIZE]

    def item_pubdate(self, obj):
        return obj.created
