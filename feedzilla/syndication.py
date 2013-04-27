# -*- coding: utf-8 -*-
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
from django.contrib.syndication.views import Feed

from django.conf import settings

from feedzilla.models import Post


class PostFeed(Feed):
    title_template = 'feedzilla/feed/post_title.html'
    description_template = 'feedzilla/feed/post_description.html'

    title = settings.FEEDZILLA_SITE_TITLE
    description = settings.FEEDZILLA_SITE_DESCRIPTION
    link = '/'

    def items(self, obj):
        return Post.active_objects.all()\
                   .order_by('-created')[:settings.FEEDZILLA_PAGE_SIZE]

    #def item_title(self, item):
        #return item.name

    #def item_description(self, item):
        #return item.description

    def item_pubdate(self, item):
        return item.created

    def item_guid(self, item):
        return str(item.guid)
