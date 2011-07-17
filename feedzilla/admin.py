# -*- coding: utf-8
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
from urlparse import urlsplit

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.http import urlencode

from feedzilla.models import Feed, Post, FilterTag, FilterWord, Request


def html_link(url):
    host = urlsplit(url).hostname
    return u'<a href="%s">%s</a>' % (url, host)


class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'last_checked',
                    'author', 'admin_feed_url', 'admin_site_url',
                    'active_post_count', 'post_count', 'created']
    search_fields = ['title', 'site_url']

    def admin_feed_url(self, obj):
        return html_link(obj.feed_url)
    admin_feed_url.allow_tags = True
    admin_feed_url.short_description = _('Feed')

    def admin_site_url(self, obj):
        return html_link(obj.site_url)
    admin_site_url.allow_tags = True
    admin_site_url.short_description = _('Site')

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'created', 'active',
                    'admin_post_link']
    list_filter = ['feed']
    search_fields = ['title', 'link', 'feed__title']

    def admin_post_link(self, obj):
        return html_link(obj.link)
    admin_post_link.allow_tags = True
    admin_post_link.short_description = _('Post link')

class FilterTagAdmin(admin.ModelAdmin):
    list_display = ['value']

class FilterWordAdmin(admin.ModelAdmin):
    list_display = ['value']


class RequestAdmin(admin.ModelAdmin):
    list_display = ['url', 'title', 'author', 'created', 'process_link']

    def process_link(self, obj):
        args = {
            'title': obj.title,
            'site_url': obj.url,
            'feed_url': obj.feed_url,
            'author': obj.author,
        }
        url = '%s?%s' % (reverse('admin:feedzilla_feed_add'),
                         urlencode(args))
        return u'<a href="%s">%s</a>' % (url, _('Process'))
    process_link.allow_tags = True
    process_link.short_description = _('Process')

admin.site.register(Feed, FeedAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(FilterTag, FilterTagAdmin)
admin.site.register(FilterWord, FilterWordAdmin)
admin.site.register(Request, RequestAdmin)
