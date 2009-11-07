# -*- coding:utf-8 -*-
from urlparse import urlsplit
import re

from django.db.models import permalink
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField

class Feed(models.Model):
    title = models.CharField(_('title'), max_length=255)
    feed_url = models.URLField(_('feed url'), unique=True, verify_exists=False)
    site_url = models.URLField(_('site url'), verify_exists=False)
    active = models.BooleanField(_('active'), blank=True, default=True)
    etag = models.CharField(u'ETag', max_length=255, blank=True, default='')
    last_checked = models.DateTimeField(_('last checked'), blank=True, null=True)
    skip_filters = models.BooleanField(_('allow all messages'), blank=True, default=False)
    author = models.CharField(_('blog author'), blank=True, max_length=255)

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


class ActivePostManager(models.Manager):
    def get_query_set(self):
        return super(ActivePostManager, self).get_query_set().filter(active=True)


class Post(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=_('feed'), related_name='posts')
    title = models.CharField(_('title'), max_length=255)
    link = models.TextField(_('link'))
    summary = models.TextField(_('summary'), blank=True)
    content = models.TextField(_('content'), blank=True)
    created = models.DateTimeField(_('creation time'))
    guid = models.CharField(_('identifier'), max_length=255, unique=True)
    tags = TagField()
    active = models.BooleanField(_('active'), blank=True, default=True)

    objects = models.Manager()
    active_objects = ActivePostManager()

    class Meta:
        ordering = ['-created']
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        #return reverse('feedzilla_post', args=[self.id])
        return self.link


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
    url = models.CharField(_('Site URL'), max_length=255, unique=True)
    created = models.DateTimeField(_('Creation date'), auto_now_add=True)

    def __unicode__(self):
        return self.url

    class Meta:
        ordering = ['-created']
        verbose_name = _('Request')
        verbose_name_plural = _('Requests')


from feedzilla import signals
signals.setup()
