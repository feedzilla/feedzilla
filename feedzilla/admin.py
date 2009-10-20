# -*- coding: utf-8

from django.contrib import admin
from feedzilla.models import Feed, Post, FilterTag, FilterWord

class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed_url', 'active', 'last_checked']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'created', 'active']

class FilterTagAdmin(admin.ModelAdmin):
    list_display = ['value']

class FilterWordAdmin(admin.ModelAdmin):
    list_display = ['value']

admin.site.register(Feed, FeedAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(FilterTag, FilterTagAdmin)
admin.site.register(FilterWord, FilterWordAdmin)
