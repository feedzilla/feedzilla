# -*- coding:utf-8 -*-
import urlparse
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

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('feed.views.feed', args=[self.id])

    class Meta:
        verbose_name = u'Фид'
        verbose_name_plural = u'Фиды'

    
class Post(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=u'Фид', related_name='posts')
    title = models.CharField(u'Заголовок', max_length=255)
    link = models.URLField(u'Ссылка', verify_exists=False)
    summary = models.TextField(u'Введение', blank=True)
    content = models.TextField(u'Содержимое', blank=True)
    created = models.DateTimeField(u'Время создания')
    guid = models.CharField(u'Идентификатор', max_length=255, unique=True)
    tags = TagField()

    class Meta:
        ordering = ['-created']
        verbose_name = u'Публикация'
        verbose_name_plural = u'Публикации'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('feedzilla_post', args=[self.id])
