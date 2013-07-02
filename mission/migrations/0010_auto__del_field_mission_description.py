# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Mission.description'
        db.delete_column(u'mission_mission', 'description')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Mission.description'
        raise RuntimeError("Cannot reverse this migration. 'Mission.description' and its values cannot be restored.")

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'kingdom.claim': {
            'Meta': {'unique_together': "(('offender', 'offended'),)", 'object_name': 'Claim'},
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offended': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offended_set'", 'to': u"orm['kingdom.Kingdom']"}),
            'offender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offender_set'", 'to': u"orm['kingdom.Kingdom']"})
        },
        u'kingdom.folk': {
            'Meta': {'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Folk'},
            'birth': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'death': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'diplomacy': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'father': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['kingdom.Folk']"}),
            'fight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kingdom.Kingdom']"}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'loyalty': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'mentor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['kingdom.Folk']"}),
            'mother': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['kingdom.Folk']"}),
            'plot': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'quality_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['kingdom.Quality']", 'null': 'True', 'blank': 'True'}),
            'scholarship': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'spouse': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['kingdom.Folk']"})
        },
        u'kingdom.kingdom': {
            'Meta': {'object_name': 'Kingdom'},
            'claims': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['kingdom.Kingdom']", 'symmetrical': 'False', 'through': u"orm['kingdom.Claim']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'population': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'prestige': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True'})
        },
        u'kingdom.quality': {
            'Meta': {'object_name': 'Quality'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kingdom.QualityCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incompatible_qualities': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'incompatible_qualities_rel_+'", 'blank': 'True', 'to': u"orm['kingdom.Quality']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'kingdom.qualitycategory': {
            'Meta': {'object_name': 'QualityCategory'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'mission._pendingmissionvariable': {
            'Meta': {'unique_together': "(('pending_mission', 'name'),)", 'object_name': '_PendingMissionVariable', 'db_table': "'mission_pendingmissionvariable'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pending_mission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mission.PendingMission']"}),
            'value': ('config.fields.stored_value.StoredValueField', [], {'max_length': '512', 'null': 'True'})
        },
        u'mission.availablemission': {
            'Meta': {'object_name': 'AvailableMission'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kingdom.Kingdom']"}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mission.Mission']"})
        },
        u'mission.mission': {
            'Meta': {'object_name': 'Mission'},
            'cancellable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': "'5'"}),
            'has_target': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'on_init': ('config.fields.script_field.ScriptField', [], {'default': "' '", 'blank': 'True'}),
            'on_resolution': ('config.fields.script_field.ScriptField', [], {'default': "' '", 'blank': 'True'}),
            'on_start': ('config.fields.script_field.ScriptField', [], {'default': "' '", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'target_description': ('django.db.models.fields.CharField', [], {'default': "'Cible'", 'max_length': '255'}),
            'target_list': ('config.fields.script_field.ScriptField', [], {'default': "' '", 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timeout': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['title.Title']", 'null': 'True', 'blank': 'True'})
        },
        u'mission.missiongrid': {
            'Meta': {'object_name': 'MissionGrid'},
            'condition': ('config.fields.script_field.ScriptField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mission.Mission']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'mission.pendingmission': {
            'Meta': {'object_name': 'PendingMission'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_started': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kingdom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kingdom.Kingdom']"}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mission.Mission']"}),
            'started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['kingdom.Kingdom']"})
        },
        u'mission.pendingmissionaffectation': {
            'Meta': {'object_name': 'PendingMissionAffectation'},
            'folk': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'mission'", 'unique': 'True', 'to': u"orm['kingdom.Folk']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission_grid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mission.MissionGrid']"}),
            'pending_mission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'folk_set'", 'to': u"orm['mission.PendingMission']"})
        },
        u'title.title': {
            'Meta': {'object_name': 'Title'},
            'condition': ('config.fields.script_field.ScriptField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'on_affect': ('config.fields.script_field.ScriptField', [], {'blank': 'True'}),
            'on_defect': ('config.fields.script_field.ScriptField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['mission']