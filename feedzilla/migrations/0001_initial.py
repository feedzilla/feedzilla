# -*- coding:utf-8 -*-

from south.db import db
from django.db import models
from feedzilla.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Feed'
        db.create_table('feedzilla_feed', (
            ('id', orm['feedzilla.Feed:id']),
            ('title', orm['feedzilla.Feed:title']),
            ('feed_url', orm['feedzilla.Feed:feed_url']),
            ('site_url', orm['feedzilla.Feed:site_url']),
            ('active', orm['feedzilla.Feed:active']),
            ('etag', orm['feedzilla.Feed:etag']),
            ('last_checked', orm['feedzilla.Feed:last_checked']),
            ('skip_filters', orm['feedzilla.Feed:skip_filters']),
        ))
        db.send_create_signal('feedzilla', ['Feed'])
        
        # Adding model 'FilterWord'
        db.create_table('feedzilla_filterword', (
            ('id', orm['feedzilla.FilterWord:id']),
            ('value', orm['feedzilla.FilterWord:value']),
            ('exact', orm['feedzilla.FilterWord:exact']),
        ))
        db.send_create_signal('feedzilla', ['FilterWord'])
        
        # Adding model 'Post'
        db.create_table('feedzilla_post', (
            ('id', orm['feedzilla.Post:id']),
            ('feed', orm['feedzilla.Post:feed']),
            ('title', orm['feedzilla.Post:title']),
            ('link', orm['feedzilla.Post:link']),
            ('summary', orm['feedzilla.Post:summary']),
            ('content', orm['feedzilla.Post:content']),
            ('created', orm['feedzilla.Post:created']),
            ('guid', orm['feedzilla.Post:guid']),
            ('tags', orm['feedzilla.Post:tags']),
            ('active', orm['feedzilla.Post:active']),
        ))
        db.send_create_signal('feedzilla', ['Post'])
        
        # Adding model 'FilterTag'
        db.create_table('feedzilla_filtertag', (
            ('id', orm['feedzilla.FilterTag:id']),
            ('value', orm['feedzilla.FilterTag:value']),
            ('exact', orm['feedzilla.FilterTag:exact']),
        ))
        db.send_create_signal('feedzilla', ['FilterTag'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Feed'
        db.delete_table('feedzilla_feed')
        
        # Deleting model 'FilterWord'
        db.delete_table('feedzilla_filterword')
        
        # Deleting model 'Post'
        db.delete_table('feedzilla_post')
        
        # Deleting model 'FilterTag'
        db.delete_table('feedzilla_filtertag')
        
    
    
    models = {
        'feedzilla.feed': {
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'etag': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'feed_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'site_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'skip_filters': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'feedzilla.filtertag': {
            'exact': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'})
        },
        'feedzilla.filterword': {
            'exact': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'})
        },
        'feedzilla.post': {
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['feedzilla.Feed']"}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['feedzilla']
