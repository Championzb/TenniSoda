# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Court.city' to match new field type.
        db.rename_column(u'court_court', 'city', 'city_id')
        # Changing field 'Court.city'
        db.alter_column(u'court_court', 'city_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['city.City']))
        # Adding index on 'Court', fields ['city']
        db.create_index(u'court_court', ['city_id'])


    def backwards(self, orm):
        # Removing index on 'Court', fields ['city']
        db.delete_index(u'court_court', ['city_id'])


        # Renaming column for 'Court.city' to match new field type.
        db.rename_column(u'court_court', 'city_id', 'city')
        # Changing field 'Court.city'
        db.alter_column(u'court_court', 'city', self.gf('django.db.models.fields.CharField')(max_length=10))

    models = {
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
        }
    }

    complete_apps = ['court']