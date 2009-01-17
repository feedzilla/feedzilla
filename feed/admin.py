# -*- coding: utf-8

from django.contrib import admin
from feed.models import Feed, Post

class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed_url', 'active', 'last_checked']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'created']


admin.site.register(Feed, FeedAdmin)
admin.site.register(Post, PostAdmin)
