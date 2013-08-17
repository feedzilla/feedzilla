# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Feed.feed_url'
        db.alter_column(u'feedzilla_feed', 'feed_url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255))

        # Changing field 'Feed.site_url'
        db.alter_column(u'feedzilla_feed', 'site_url', self.gf('django.db.models.fields.CharField')(max_length=255))
        # Deleting field 'Post.tags'
        db.delete_column(u'feedzilla_post', 'tags')


    def backwards(self, orm):

        # Changing field 'Feed.feed_url'
        db.alter_column(u'feedzilla_feed', 'feed_url', self.gf('django.db.models.fields.URLField')(max_length=200, unique=True))

        # Changing field 'Feed.site_url'
        db.alter_column(u'feedzilla_feed', 'site_url', self.gf('django.db.models.fields.URLField')(max_length=200))
        # Adding field 'Post.tags'
        db.add_column(u'feedzilla_post', 'tags',
                      self.gf('tagging.fields.TagField')(default=''),
                      keep_default=False)

    complete_apps = ['feedzilla']
