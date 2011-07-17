# encoding: utf-8
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Feed'
        db.create_table('feedzilla_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('feed_url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('site_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('etag', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('last_checked', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('skip_filters', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('feedzilla', ['Feed'])

        # Adding model 'Post'
        db.create_table('feedzilla_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['feedzilla.Feed'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('link', self.gf('django.db.models.fields.TextField')()),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('guid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('feedzilla', ['Post'])

        # Adding model 'FilterTag'
        db.create_table('feedzilla_filtertag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('exact', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('feedzilla', ['FilterTag'])

        # Adding model 'FilterWord'
        db.create_table('feedzilla_filterword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('exact', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('feedzilla', ['FilterWord'])

        # Adding model 'Request'
        db.create_table('feedzilla_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('feed_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('feedzilla', ['Request'])


    def backwards(self, orm):
        
        # Deleting model 'Feed'
        db.delete_table('feedzilla_feed')

        # Deleting model 'Post'
        db.delete_table('feedzilla_post')

        # Deleting model 'FilterTag'
        db.delete_table('feedzilla_filtertag')

        # Deleting model 'FilterWord'
        db.delete_table('feedzilla_filterword')

        # Deleting model 'Request'
        db.delete_table('feedzilla_request')


    models = {
        'feedzilla.feed': {
            'Meta': {'object_name': 'Feed'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'etag': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'feed_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'site_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'skip_filters': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'feedzilla.filtertag': {
            'Meta': {'object_name': 'FilterTag'},
            'exact': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'feedzilla.filterword': {
            'Meta': {'object_name': 'FilterWord'},
            'exact': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'feedzilla.post': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Post'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['feedzilla.Feed']"}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'feedzilla.request': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Request'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feed_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['feedzilla']
