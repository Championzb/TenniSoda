# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'League'
        db.create_table(u'game_league', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['city.City'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('max_player_number', self.gf('django.db.models.fields.IntegerField')()),
            ('level_low', self.gf('django.db.models.fields.FloatField')()),
            ('level_high', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'game', ['League'])

        # Adding M2M table for field players on 'League'
        m2m_table_name = db.shorten_name(u'game_league_players')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('league', models.ForeignKey(orm[u'game.league'], null=False)),
            ('account', models.ForeignKey(orm[u'account.account'], null=False))
        ))
        db.create_unique(m2m_table_name, ['league_id', 'account_id'])

        # Adding model 'Game'
        db.create_table(u'game_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.League'], null=True, blank=True)),
            ('court', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['court.Court'], null=True, blank=True)),
            ('player1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player1', to=orm['account.Account'])),
            ('player2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player2', to=orm['account.Account'])),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='winnner', to=orm['account.Account'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('player1_rated', self.gf('django.db.models.fields.IntegerField')()),
            ('player2_rated', self.gf('django.db.models.fields.IntegerField')()),
            ('player1_reviewed', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
            ('player2_reviewed', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True, blank=True)),
            ('court_review1', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='court_review1', null=True, to=orm['review.CourtReview'])),
            ('court_review2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='court_review2', null=True, to=orm['review.CourtReview'])),
        ))
        db.send_create_signal(u'game', ['Game'])

        # Adding model 'Score'
        db.create_table(u'game_score', (
            ('game', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['game.Game'], unique=True, primary_key=True)),
            ('score11', self.gf('django.db.models.fields.IntegerField')()),
            ('score12', self.gf('django.db.models.fields.IntegerField')()),
            ('score21', self.gf('django.db.models.fields.IntegerField')()),
            ('score22', self.gf('django.db.models.fields.IntegerField')()),
            ('score31', self.gf('django.db.models.fields.IntegerField')()),
            ('score32', self.gf('django.db.models.fields.IntegerField')()),
            ('score41', self.gf('django.db.models.fields.IntegerField')()),
            ('score42', self.gf('django.db.models.fields.IntegerField')()),
            ('score51', self.gf('django.db.models.fields.IntegerField')()),
            ('score52', self.gf('django.db.models.fields.IntegerField')()),
            ('is_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'game', ['Score'])


    def backwards(self, orm):
        # Deleting model 'League'
        db.delete_table(u'game_league')

        # Removing M2M table for field players on 'League'
        db.delete_table(db.shorten_name(u'game_league_players'))

        # Deleting model 'Game'
        db.delete_table(u'game_game')

        # Deleting model 'Score'
        db.delete_table(u'game_score')


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
        u'game.game': {
            'Meta': {'object_name': 'Game'},
            'court': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['court.Court']", 'null': 'True', 'blank': 'True'}),
            'court_review1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'court_review1'", 'null': 'True', 'to': u"orm['review.CourtReview']"}),
            'court_review2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'court_review2'", 'null': 'True', 'to': u"orm['review.CourtReview']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.League']", 'null': 'True', 'blank': 'True'}),
            'player1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player1'", 'to': u"orm['account.Account']"}),
            'player1_rated': ('django.db.models.fields.IntegerField', [], {}),
            'player1_reviewed': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'player2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player2'", 'to': u"orm['account.Account']"}),
            'player2_rated': ('django.db.models.fields.IntegerField', [], {}),
            'player2_reviewed': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'winnner'", 'to': u"orm['account.Account']"})
        },
        u'game.league': {
            'Meta': {'object_name': 'League'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['city.City']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level_high': ('django.db.models.fields.FloatField', [], {}),
            'level_low': ('django.db.models.fields.FloatField', [], {}),
            'max_player_number': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['account.Account']", 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'game.score': {
            'Meta': {'object_name': 'Score'},
            'game': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['game.Game']", 'unique': 'True', 'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'score11': ('django.db.models.fields.IntegerField', [], {}),
            'score12': ('django.db.models.fields.IntegerField', [], {}),
            'score21': ('django.db.models.fields.IntegerField', [], {}),
            'score22': ('django.db.models.fields.IntegerField', [], {}),
            'score31': ('django.db.models.fields.IntegerField', [], {}),
            'score32': ('django.db.models.fields.IntegerField', [], {}),
            'score41': ('django.db.models.fields.IntegerField', [], {}),
            'score42': ('django.db.models.fields.IntegerField', [], {}),
            'score51': ('django.db.models.fields.IntegerField', [], {}),
            'score52': ('django.db.models.fields.IntegerField', [], {})
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

    complete_apps = ['game']