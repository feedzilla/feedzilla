# -*- coding:utf-8 -*-
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
from urlparse import urlsplit
import re
from grab.tools.lxml_tools import clean_html

# Compatibility with transliterate < 1.4
try:
    from transliterate import autodiscover
except ImportError:
    pass
else:
    autodiscover()

from transliterate.utils import translit

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.text import slugify

from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase


class Feed(models.Model):
    title = models.CharField(_('title'), max_length=255)
    feed_url = models.CharField(_('feed url'), max_length=255, unique=True)
    site_url = models.CharField(_('site url'), max_length=255)
    active = models.BooleanField(_('active'), blank=True, default=True, db_index=True)
    etag = models.CharField(u'ETag', max_length=255, blank=True, default='')
    last_checked = models.DateTimeField(_('last checked'), blank=True, null=True)
    skip_filters = models.BooleanField(_('allow all messages'), blank=True, default=False)
    author = models.CharField(_('blog author'), blank=True, max_length=255)
    created = models.DateTimeField(_('Date of submition'), blank=True, null=True,
                                   auto_now_add=True, db_index=True)
    post_count = models.IntegerField(blank=True, default=0)
    active_post_count = models.IntegerField(blank=True, default=0)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('feedzilla_feed', args=[self.id])

    def site_hostname(self):
        return urlsplit(self.site_url).hostname

    class Meta:
        verbose_name = _('feed')
        verbose_name_plural = _('feeds')

    def author_or_title(self):
        return self.author or self.title

    def update_counts(self):
        self.post_count = self.posts.count()
        self.active_post_count = self.posts.filter(active=True).count()
        self.save()


class ActivePostManager(models.Manager):
    def get_query_set(self):
        return super(ActivePostManager, self).get_query_set().filter(active=True)


class FeedzillaTag(TagBase):
    """
    Custom version of Tag that
    knows how to bild slugs for Russian words
    """
    def slugify(self, tag, i=None):
            slug = slugify(translit(tag, 'ru', reversed=True))
            if i is not None:
                slug += "-%d" % i
            return slug


class FeedzillaTagItem(GenericTaggedItemBase):
    tag = models.ForeignKey(FeedzillaTag, related_name='items')


class Post(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=_('feed'), related_name='posts')
    title = models.CharField(_('title'), max_length=255)
    link = models.TextField(_('link'))
    summary = models.TextField(_('summary'), blank=True)
    content = models.TextField(_('content'), blank=True)
    created = models.DateTimeField(_('creation time'))
    guid = models.CharField(_('identifier'), max_length=255, unique=True)
    active = models.BooleanField(_('active'), blank=True, default=True)

    objects = models.Manager()
    active_objects = ActivePostManager()
    tags = TaggableManager(through=FeedzillaTagItem)
    rawtags = models.CharField(max_length=255)

    class Meta:
        ordering = ['-created']
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        #return reverse('feedzilla_post', args=[self.id])
        return self.link

    def summary_uncached(self):
        return clean_html(self.content[:settings.FEEDZILLA_SUMMARY_SIZE])


class FilterTag(models.Model):
    value = models.CharField(_('Value'), max_length=255, unique=True)
    exact = models.BooleanField(_('Exact match'), blank=True, default=False)

    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = _('Filter tag')
        verbose_name_plural = _('Filter tags')


class FilterWord(models.Model):
    value = models.CharField(_('Value'), max_length=255, unique=True)
    exact = models.BooleanField(_('Exact match'), blank=True, default=False)

    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = _('Filter word')
        verbose_name_plural = _('Filter words')


class Request(models.Model):
    url = models.CharField(_('Blog URL'), max_length=255, unique=True)
    title = models.CharField(_('Blog name'), max_length=255)
    author = models.CharField(_('Name of author of the blog'), blank=True, max_length=50)
    feed_url = models.CharField(_('Feed URL'), blank=True, max_length=255, help_text=_('You can specify what exactly feed you want submit'))
    created = models.DateTimeField(_('Creation date'), auto_now_add=True)

    def __unicode__(self):
        return self.url

    class Meta:
        ordering = ['-created']
        verbose_name = _('Request')
        verbose_name_plural = _('Requests')


from feedzilla import signals
signals.setup()
