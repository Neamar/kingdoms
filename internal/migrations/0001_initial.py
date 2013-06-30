# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Trigger'
        db.create_table(u'internal_trigger', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('prestige_threshold', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('population_threshold', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('money_threshold', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('condition', self.gf('vendors.code_field.fields.ScriptField')(default='', null=True, blank=True)),
            ('on_fire', self.gf('vendors.code_field.fields.ScriptField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'internal', ['Trigger'])

        # Adding M2M table for field fired on 'Trigger'
        m2m_table_name = db.shorten_name(u'internal_trigger_fired')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('trigger', models.ForeignKey(orm[u'internal.trigger'], null=False)),
            ('kingdom', models.ForeignKey(orm[u'kingdom.kingdom'], null=False))
        ))
        db.create_unique(m2m_table_name, ['trigger_id', 'kingdom_id'])

        # Adding model 'Constant'
        db.create_table(u'internal_constant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'internal', ['Constant'])

        # Adding model 'Value'
        db.create_table(u'internal_value', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('kingdom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kingdom.Kingdom'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('expiration', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'internal', ['Value'])

        # Adding unique constraint on 'Value', fields ['name', 'kingdom']
        db.create_unique(u'internal_value', ['name', 'kingdom_id'])

        # Adding model 'Recurring'
        db.create_table(u'internal_recurring', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('frequency', self.gf('django.db.models.fields.CharField')(default='hourly', max_length=8)),
            ('condition', self.gf('vendors.code_field.fields.ScriptField')(null=True, blank=True)),
            ('on_fire', self.gf('vendors.code_field.fields.ScriptField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'internal', ['Recurring'])

        # Adding model 'FirstName'
        db.create_table(u'internal_firstname', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'internal', ['FirstName'])

        # Adding model 'LastName'
        db.create_table(u'internal_lastname', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'internal', ['LastName'])


    def backwards(self, orm):
        # Removing unique constraint on 'Value', fields ['name', 'kingdom']
        db.delete_unique(u'internal_value', ['name', 'kingdom_id'])

        # Deleting model 'Trigger'
        db.delete_table(u'internal_trigger')

        # Removing M2M table for field fired on 'Trigger'
        db.delete_table(db.shorten_name(u'internal_trigger_fired'))

        # Deleting model 'Constant'
        db.delete_table(u'internal_constant')

        # Deleting model 'Value'
        db.delete_table(u'internal_value')

        # Deleting model 'Recurring'
        db.delete_table(u'internal_recurring')

        # Deleting model 'FirstName'
        db.delete_table(u'internal_firstname')

        # Deleting model 'LastName'
        db.delete_table(u'internal_lastname')


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
        u'internal.constant': {
            'Meta': {'object_name': 'Constant'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'internal.firstname': {
            'Meta': {'object_name': 'FirstName'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'internal.lastname': {
            'Meta': {'object_name': 'LastName'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'internal.recurring': {
            'Meta': {'object_name': 'Recurring'},
            'condition': ('vendors.code_field.fields.ScriptField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'frequency': ('django.db.models.fields.CharField', [], {'default': "'hourly'", 'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'on_fire': ('vendors.code_field.fields.ScriptField', [], {'null': 'True', 'blank': 'True'})
        },
        u'internal.trigger': {
            'Meta': {'object_name': 'Trigger'},
            'condition': ('vendors.code_field.fields.ScriptField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fired': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['kingdom.Kingdom']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money_threshold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'on_fire': ('vendors.code_field.fields.ScriptField', [], {'null': 'True', 'blank': 'True'}),
            'population_threshold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'prestige_threshold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'internal.value': {
            'Meta': {'unique_together': "(('name', 'kingdom'),)", 'object_name': 'Value'},
            'expiration': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kingdom.Kingdom']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'kingdom.claim': {
            'Meta': {'unique_together': "(('offender', 'offended'),)", 'object_name': 'Claim'},
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offended': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offended_set'", 'to': u"orm['kingdom.Kingdom']"}),
            'offender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offender_set'", 'to': u"orm['kingdom.Kingdom']"})
        },
        u'kingdom.kingdom': {
            'Meta': {'object_name': 'Kingdom'},
            'claims': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['kingdom.Kingdom']", 'symmetrical': 'False', 'through': u"orm['kingdom.Claim']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'population': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'prestige': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        }
    }

    complete_apps = ['internal']