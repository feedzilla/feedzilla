# -*- coding: utf-8 -*-
import os
from datetime import datetime

from django.contrib.syndication.feeds import FeedDoesNotExist
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.conf import settings

from feed.models import Post

class PostFeed(Feed):
    feed_type = Atom1Feed
    link = '/posts/'
    title = u'Новости семантического веба'

    #def item_link(self, obj):
        #return obj.get_imdb_link()

    def item_guid(self, obj):
        return str(obj.guid)

    def items(self, obj):
        return Post.objects.all().order_by('-created')

    def item_pubdate(self, obj):
        return obj.created
