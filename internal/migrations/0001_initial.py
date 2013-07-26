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
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('prestige_threshold', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('population_threshold', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('money_threshold', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('condition', self.gf('config.fields.script_field.ScriptField')(default=None, null=True, blank=True)),
            ('on_fire', self.gf('config.fields.script_field.ScriptField')(default=None, null=True, blank=True)),
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

        # Adding model 'Recurring'
        db.create_table(u'internal_recurring', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('delay', self.gf('django.db.models.fields.PositiveIntegerField')(default=144)),
            ('condition', self.gf('config.fields.script_field.ScriptField')(default=None, null=True, blank=True)),
            ('on_fire', self.gf('config.fields.script_field.ScriptField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'internal', ['Recurring'])

        # Adding model 'Function'
        db.create_table(u'internal_function', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('on_fire', self.gf('config.fields.script_field.ScriptField')(default='')),
        ))
        db.send_create_signal(u'internal', ['Function'])

        # Adding model 'FirstName'
        db.create_table(u'internal_firstname', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('sex', self.gf('django.db.models.fields.CharField')(default='m', max_length=1)),
        ))
        db.send_create_signal(u'internal', ['FirstName'])

        # Adding model 'LastName'
        db.create_table(u'internal_lastname', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'internal', ['LastName'])

        # Adding model 'Avatar'
        db.create_table(u'internal_avatar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(default='m', max_length=1)),
            ('hair', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('fight', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('diplomacy', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('plot', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('scholarship', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('child', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, blank=True)),
            ('adult', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, blank=True)),
            ('old', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, blank=True)),
            ('adult_threshold', self.gf('django.db.models.fields.PositiveIntegerField')(default=16)),
            ('old_threshold', self.gf('django.db.models.fields.PositiveIntegerField')(default=45)),
        ))
        db.send_create_signal(u'internal', ['Avatar'])

        # Adding M2M table for field qualities on 'Avatar'
        m2m_table_name = db.shorten_name(u'internal_avatar_qualities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('avatar', models.ForeignKey(orm[u'internal.avatar'], null=False)),
            ('quality', models.ForeignKey(orm[u'kingdom.quality'], null=False))
        ))
        db.create_unique(m2m_table_name, ['avatar_id', 'quality_id'])

        # Adding model 'ScriptLog'
        db.create_table(u'internal_scriptlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kingdom', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['kingdom.Kingdom'], null=True, on_delete=models.SET_NULL)),
            ('object_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('object_pk', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('object_attr', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('stack_level', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('direct_queries', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
            ('queries', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True)),
        ))
        db.send_create_signal(u'internal', ['ScriptLog'])


    def backwards(self, orm):
        # Deleting model 'Trigger'
        db.delete_table(u'internal_trigger')

        # Removing M2M table for field fired on 'Trigger'
        db.delete_table(db.shorten_name(u'internal_trigger_fired'))

        # Deleting model 'Constant'
        db.delete_table(u'internal_constant')

        # Deleting model 'Recurring'
        db.delete_table(u'internal_recurring')

        # Deleting model 'Function'
        db.delete_table(u'internal_function')

        # Deleting model 'FirstName'
        db.delete_table(u'internal_firstname')

        # Deleting model 'LastName'
        db.delete_table(u'internal_lastname')

        # Deleting model 'Avatar'
        db.delete_table(u'internal_avatar')

        # Removing M2M table for field qualities on 'Avatar'
        db.delete_table(db.shorten_name(u'internal_avatar_qualities'))

        # Deleting model 'ScriptLog'
        db.delete_table(u'internal_scriptlog')


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
        u'internal.avatar': {
            'Meta': {'object_name': 'Avatar'},
            'adult': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'blank': 'True'}),
            'adult_threshold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '16'}),
            'child': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'blank': 'True'}),
            'diplomacy': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fight': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hair': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'blank': 'True'}),
            'old_threshold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '45'}),
            'plot': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'qualities': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['kingdom.Quality']", 'symmetrical': 'False', 'blank': 'True'}),
            'scholarship': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'})
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'})
        },
        u'internal.function': {
            'Meta': {'object_name': 'Function'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'on_fire': ('config.fields.script_field.ScriptField', [], {'default': "''"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'internal.lastname': {
            'Meta': {'object_name': 'LastName'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'internal.recurring': {
            'Meta': {'object_name': 'Recurring'},
            'condition': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'delay': ('django.db.models.fields.PositiveIntegerField', [], {'default': '144'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'on_fire': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'internal.scriptlog': {
            'Meta': {'object_name': 'ScriptLog'},
            'direct_queries': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdom': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['kingdom.Kingdom']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'object_attr': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'object_pk': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'object_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'queries': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'stack_level': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'internal.trigger': {
            'Meta': {'object_name': 'Trigger'},
            'condition': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fired': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['kingdom.Kingdom']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money_threshold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'on_fire': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'population_threshold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'prestige_threshold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'kingdom.claim': {
            'Meta': {'unique_together': "(('offender', 'offended'),)", 'object_name': 'Claim'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
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
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True'})
        },
        u'kingdom.quality': {
            'Meta': {'object_name': 'Quality'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kingdom.QualityCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'female_description': ('django.db.models.fields.TextField', [], {}),
            'female_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incompatible_qualities': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'incompatible_qualities_rel_+'", 'blank': 'True', 'to': u"orm['kingdom.Quality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'on_affect': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'on_defect': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'kingdom.qualitycategory': {
            'Meta': {'object_name': 'QualityCategory'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['internal']