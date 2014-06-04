# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table(u'account_profile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['account.Account'], unique=True, primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('level', self.gf('django.db.models.fields.CharField')(default='3', max_length=15)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('city', self.gf('django.db.models.fields.CharField')(default='1', max_length=3)),
        ))
        db.send_create_signal(u'account', ['Profile'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table(u'account_profile')


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
        u'account.profile': {
            'Meta': {'object_name': 'Profile'},
            'city': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '3'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'level': ('django.db.models.fields.CharField', [], {'default': "'3'", 'max_length': '15'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['account.Account']", 'unique': 'True', 'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['account']