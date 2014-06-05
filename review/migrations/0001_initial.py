# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CourtReview'
        db.create_table(u'review_courtreview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('court', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['court.Court'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Account'])),
            ('review', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('rate', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'review', ['CourtReview'])


    def backwards(self, orm):
        # Deleting model 'CourtReview'
        db.delete_table(u'review_courtreview')


    models = {
        u'account.account': {
            'Meta': {'object_name': 'Account'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'city.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'court.court': {
            'Meta': {'object_name': 'Court'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['city.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_free': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'review.courtreview': {
            'Meta': {'object_name': 'CourtReview'},
            'court': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['court.Court']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.IntegerField', [], {}),
            'review': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Account']"})
        }
    }

    complete_apps = ['review']