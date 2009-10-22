# -*- coding:utf-8 -*-
from urlparse import urlsplit
import re

from django.db.models import permalink
from django.db import models
from django.core.urlresolvers import reverse

from tagging.fields import TagField

class Feed(models.Model):
    title = models.CharField(u'Название', max_length=255)
    feed_url = models.URLField(u'Адрес фида', unique=True, verify_exists=False)
    site_url = models.URLField(u'Адрес сайта', verify_exists=False)
    active = models.BooleanField(u'Активен', blank=True, default=True)
    etag = models.CharField(u'ETag', max_length=255, blank=True, default='')
    last_checked = models.DateTimeField(u'Время пооследней проверки', blank=True, null=True)
    skip_filters = models.BooleanField(u'Разрешать все сообщения', blank=True, default=False)
    author = models.CharField('Автор блога', blank=True, max_length=255)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('feedzilla_feed', args=[self.id])

    def site_hostname(self):
        return urlsplit(self.site_url).hostname

    class Meta:
        verbose_name = u'Фид'
        verbose_name_plural = u'Фиды'

    def author_or_title(self):
        return self.author or self.title

   
class ActivePostManager(models.Manager):
    def get_query_set(self):
        return super(ActivePostManager, self).get_query_set().filter(active=True)


class Post(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=u'Фид', related_name='posts')
    title = models.CharField(u'Заголовок', max_length=255)
    link = models.TextField(u'Ссылка')
    summary = models.TextField(u'Введение', blank=True)
    content = models.TextField(u'Содержимое', blank=True)
    created = models.DateTimeField(u'Время создания')
    guid = models.CharField(u'Идентификатор', max_length=255, unique=True)
    tags = TagField()
    active = models.BooleanField(u'Активен', blank=True, default=True)

    objects = models.Manager()
    active_objects = ActivePostManager()

    class Meta:
        ordering = ['-created']
        verbose_name = u'Публикация'
        verbose_name_plural = u'Публикации'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        #return reverse('feedzilla_post', args=[self.id])
        return self.link


class FilterTag(models.Model):
    value = models.CharField(max_length=255, unique=True)
    exact = models.BooleanField(blank=True, default=False)

    def __unicode__(self):
        return self.value


class FilterWord(models.Model):
    value = models.CharField(max_length=255, unique=True)
    exact = models.BooleanField(blank=True, default=False)

    def __unicode__(self):
        return self.value


class Request(models.Model):
    url = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.url

    class Meta:
        ordering = ['-created']


from feedzilla import signals
signals.setup()
