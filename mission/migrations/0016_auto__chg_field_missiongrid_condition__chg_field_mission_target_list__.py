# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'MissionGrid.condition'
        db.alter_column('mission_missiongrid', 'condition', self.gf('config.fields.script_field.ScriptField')(null=True))

        # Changing field 'Mission.target_list'
        db.alter_column('mission_mission', 'target_list', self.gf('config.fields.script_field.ScriptField')(null=True))

        # Changing field 'Mission.on_start'
        db.alter_column('mission_mission', 'on_start', self.gf('config.fields.script_field.ScriptField')(null=True))

        # Changing field 'Mission.on_init'
        db.alter_column('mission_mission', 'on_init', self.gf('config.fields.script_field.ScriptField')(null=True))

        # Changing field 'Mission.on_resolution'
        db.alter_column('mission_mission', 'on_resolution', self.gf('config.fields.script_field.ScriptField')(null=True))

    def backwards(self, orm):

        # Changing field 'MissionGrid.condition'
        db.alter_column('mission_missiongrid', 'condition', self.gf('config.fields.script_field.ScriptField')())

        # Changing field 'Mission.target_list'
        db.alter_column('mission_mission', 'target_list', self.gf('config.fields.script_field.ScriptField')())

        # Changing field 'Mission.on_start'
        db.alter_column('mission_mission', 'on_start', self.gf('config.fields.script_field.ScriptField')())

        # Changing field 'Mission.on_init'
        db.alter_column('mission_mission', 'on_init', self.gf('config.fields.script_field.ScriptField')())

        # Changing field 'Mission.on_resolution'
        db.alter_column('mission_mission', 'on_resolution', self.gf('config.fields.script_field.ScriptField')())

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'internal.avatar': {
            'Meta': {'object_name': 'Avatar'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['internal.AvatarCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'internal.avatarcategory': {
            'Meta': {'object_name': 'AvatarCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'kingdom.claim': {
            'Meta': {'unique_together': "(('offender', 'offended'),)", 'object_name': 'Claim'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'offended': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offended_set'", 'to': "orm['kingdom.Kingdom']"}),
            'offender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offender_set'", 'to': "orm['kingdom.Kingdom']"})
        },
        'kingdom.folk': {
            'Meta': {'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Folk'},
            'avatar': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['internal.Avatar']", 'null': 'True', 'blank': 'True'}),
            'birth': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'death': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'diplomacy': ('django.db.models.fields.PositiveIntegerField', [], {'default': '7'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'father': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['kingdom.Folk']"}),
            'fight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '7'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kingdom.Kingdom']"}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'loyalty': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'mentor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['kingdom.Folk']"}),
            'mother': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['kingdom.Folk']"}),
            'plot': ('django.db.models.fields.PositiveIntegerField', [], {'default': '7'}),
            'quality_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['kingdom.Quality']", 'null': 'True', 'blank': 'True'}),
            'scholarship': ('django.db.models.fields.PositiveIntegerField', [], {'default': '7'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'spouse': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['kingdom.Folk']"})
        },
        'kingdom.kingdom': {
            'Meta': {'object_name': 'Kingdom'},
            'claims': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['kingdom.Kingdom']", 'symmetrical': 'False', 'through': "orm['kingdom.Claim']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'population': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'prestige': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'})
        },
        'kingdom.quality': {
            'Meta': {'object_name': 'Quality'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kingdom.QualityCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incompatible_qualities': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'incompatible_qualities_rel_+'", 'blank': 'True', 'to': "orm['kingdom.Quality']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'on_affect': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'on_defect': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'kingdom.qualitycategory': {
            'Meta': {'object_name': 'QualityCategory'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'mission._pendingmissionvariable': {
            'Meta': {'unique_together': "(('pending_mission', 'name'),)", 'object_name': '_PendingMissionVariable', 'db_table': "'mission_pendingmissionvariable'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pending_mission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mission.PendingMission']"}),
            'value': ('config.fields.stored_value.StoredValueField', [], {'max_length': '1024', 'null': 'True'})
        },
        'mission.availablemission': {
            'Meta': {'unique_together': "(('mission', 'kingdom'),)", 'object_name': 'AvailableMission'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kingdom.Kingdom']"}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mission.Mission']"})
        },
        'mission.mission': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Mission'},
            'cancellable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': "'5'"}),
            'has_target': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_value': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'on_init': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'on_resolution': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'on_start': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'target_description': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True'}),
            'target_list': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timeout': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['title.Title']", 'null': 'True', 'blank': 'True'}),
            'value_description': ('django.db.models.fields.CharField', [], {'default': "'Valeur :'", 'max_length': '255'})
        },
        'mission.missiongrid': {
            'Meta': {'ordering': "['mission__name']", 'object_name': 'MissionGrid'},
            'condition': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mission.Mission']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'mission.pendingmission': {
            'Meta': {'object_name': 'PendingMission'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_started': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kingdom': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kingdom.Kingdom']"}),
            'last_target': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'+'", 'null': 'True', 'to': "orm['kingdom.Kingdom']"}),
            'last_value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mission.Mission']"}),
            'started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['kingdom.Kingdom']"}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'mission.pendingmissionaffectation': {
            'Meta': {'object_name': 'PendingMissionAffectation'},
            'folk': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'mission'", 'unique': 'True', 'to': "orm['kingdom.Folk']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission_grid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mission.MissionGrid']"}),
            'pending_mission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'folk_set'", 'to': "orm['mission.PendingMission']"})
        },
        'title.title': {
            'Meta': {'object_name': 'Title'},
            'condition': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'on_affect': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'on_defect': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'on_unlock': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['mission']