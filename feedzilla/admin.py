# -*- coding: utf-8

from django.contrib import admin
from feedzilla.models import Feed, Post, FilterTag, FilterWord, Request

class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'last_checked',
                    'admin_feed_url', 'admin_site_url']
    search_fields = ['title', 'site_url']

    def admin_feed_url(self, obj):
        return u'<a href="%s">ссылка</a>' % obj.feed_url
    admin_feed_url.allow_tags = True

    def admin_site_url(self, obj):
        return u'<a href="%s">ссылка</a>' % obj.site_url
    admin_site_url.allow_tags = True

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'created', 'active',
                    'admin_post_link']
    list_filter = ['feed']
    search_fields = ['title', 'link', 'feed__title']

    def admin_post_link(self, obj):
        return u'<a href="%s">ссылка</a>' % obj.link
    admin_post_link.allow_tags = True

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
