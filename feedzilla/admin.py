# -*- coding: utf-8

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from feedzilla.models import Feed, Post, FilterTag, FilterWord, Request


def html_link(link):
    return u'<a href="%(link)s">%(label)s</a>' % {'link': link, 'label': _('link')}


class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'last_checked',
                    'admin_feed_url', 'admin_site_url']
    search_fields = ['title', 'site_url']

    def admin_feed_url(self, obj):
        return html_link(obj.feed_url)
    admin_feed_url.allow_tags = True
    admin_feed_url.short_description = _('Feed link')

    def admin_site_url(self, obj):
        return html_link(obj.site_url)
    admin_site_url.allow_tags = True
    admin_site_url.short_description = _('Site link')

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
    list_display = ['url', 'created']

admin.site.register(Feed, FeedAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(FilterTag, FilterTagAdmin)
admin.site.register(FilterWord, FilterWordAdmin)
admin.site.register(Request, RequestAdmin)
