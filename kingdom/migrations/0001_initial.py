# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Kingdom'
        db.create_table(u'kingdom_kingdom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True)),
            ('prestige', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('population', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('money', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'kingdom', ['Kingdom'])

        # Adding model '_KingdomVariable'
        db.create_table('kingdom_kingdomvariable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('kingdom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kingdom.Kingdom'])),
            ('value', self.gf('config.fields.stored_value.StoredValueField')(max_length=1024, null=True)),
        ))
        db.send_create_signal(u'kingdom', ['_KingdomVariable'])

        # Adding unique constraint on '_KingdomVariable', fields ['name', 'kingdom']
        db.create_unique('kingdom_kingdomvariable', ['name', 'kingdom_id'])

        # Adding model 'Folk'
        db.create_table(u'kingdom_folk', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kingdom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kingdom.Kingdom'], null=True)),
            ('avatar', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['internal.Avatar'], null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(default='m', max_length=1)),
            ('mother', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['kingdom.Folk'])),
            ('father', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['kingdom.Folk'])),
            ('spouse', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['kingdom.Folk'])),
            ('mentor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['kingdom.Folk'])),
            ('birth', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('death', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('fight', self.gf('django.db.models.fields.PositiveIntegerField')(default=7)),
            ('diplomacy', self.gf('django.db.models.fields.PositiveIntegerField')(default=7)),
            ('plot', self.gf('django.db.models.fields.PositiveIntegerField')(default=7)),
            ('scholarship', self.gf('django.db.models.fields.PositiveIntegerField')(default=7)),
            ('loyalty', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('disabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'kingdom', ['Folk'])

        # Adding unique constraint on 'Folk', fields ['first_name', 'last_name']
        db.create_unique(u'kingdom_folk', ['first_name', 'last_name'])

        # Adding M2M table for field quality_set on 'Folk'
        m2m_table_name = db.shorten_name(u'kingdom_folk_quality_set')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('folk', models.ForeignKey(orm[u'kingdom.folk'], null=False)),
            ('quality', models.ForeignKey(orm[u'kingdom.quality'], null=False))
        ))
        db.create_unique(m2m_table_name, ['folk_id', 'quality_id'])

        # Adding model 'QualityCategory'
        db.create_table(u'kingdom_qualitycategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'kingdom', ['QualityCategory'])

        # Adding model 'Quality'
        db.create_table(u'kingdom_quality', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('female_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('female_description', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kingdom.QualityCategory'])),
            ('on_affect', self.gf('config.fields.script_field.ScriptField')(default=None, null=True, blank=True)),
            ('on_defect', self.gf('config.fields.script_field.ScriptField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'kingdom', ['Quality'])

        # Adding M2M table for field incompatible_qualities on 'Quality'
        m2m_table_name = db.shorten_name(u'kingdom_quality_incompatible_qualities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_quality', models.ForeignKey(orm[u'kingdom.quality'], null=False)),
            ('to_quality', models.ForeignKey(orm[u'kingdom.quality'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_quality_id', 'to_quality_id'])

        # Adding model 'Message'
        db.create_table(u'kingdom_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kingdom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kingdom.Kingdom'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('level', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('read', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'kingdom', ['Message'])

        # Adding model 'ModalMessage'
        db.create_table(u'kingdom_modalmessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('kingdom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kingdom.Kingdom'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'kingdom', ['ModalMessage'])

        # Adding model 'Claim'
        db.create_table(u'kingdom_claim', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('offender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='offender_set', to=orm['kingdom.Kingdom'])),
            ('offended', self.gf('django.db.models.fields.related.ForeignKey')(related_name='offended_set', to=orm['kingdom.Kingdom'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('level', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'kingdom', ['Claim'])

        # Adding unique constraint on 'Claim', fields ['offender', 'offended']
        db.create_unique(u'kingdom_claim', ['offender_id', 'offended_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Claim', fields ['offender', 'offended']
        db.delete_unique(u'kingdom_claim', ['offender_id', 'offended_id'])

        # Removing unique constraint on 'Folk', fields ['first_name', 'last_name']
        db.delete_unique(u'kingdom_folk', ['first_name', 'last_name'])

        # Removing unique constraint on '_KingdomVariable', fields ['name', 'kingdom']
        db.delete_unique('kingdom_kingdomvariable', ['name', 'kingdom_id'])

        # Deleting model 'Kingdom'
        db.delete_table(u'kingdom_kingdom')

        # Deleting model '_KingdomVariable'
        db.delete_table('kingdom_kingdomvariable')

        # Deleting model 'Folk'
        db.delete_table(u'kingdom_folk')

        # Removing M2M table for field quality_set on 'Folk'
        db.delete_table(db.shorten_name(u'kingdom_folk_quality_set'))

        # Deleting model 'QualityCategory'
        db.delete_table(u'kingdom_qualitycategory')

        # Deleting model 'Quality'
        db.delete_table(u'kingdom_quality')

        # Removing M2M table for field incompatible_qualities on 'Quality'
        db.delete_table(db.shorten_name(u'kingdom_quality_incompatible_qualities'))

        # Deleting model 'Message'
        db.delete_table(u'kingdom_message')

        # Deleting model 'ModalMessage'
        db.delete_table(u'kingdom_modalmessage')

        # Deleting model 'Claim'
        db.delete_table(u'kingdom_claim')


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
        u'kingdom._kingdomvariable': {
            'Meta': {'unique_together': "(('name', 'kingdom'),)", 'object_name': '_KingdomVariable', 'db_table': "'kingdom_kingdomvariable'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kingdom.Kingdom']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('config.fields.stored_value.StoredValueField', [], {'max_length': '1024', 'null': 'True'})
        },
        u'kingdom.claim': {
            'Meta': {'unique_together': "(('offender', 'offended'),)", 'object_name': 'Claim'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'offended': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offended_set'", 'to': u"orm['kingdom.Kingdom']"}),
            'offender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offender_set'", 'to': u"orm['kingdom.Kingdom']"})
        },
        u'kingdom.folk': {
            'Meta': {'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Folk'},
            'avatar': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['internal.Avatar']", 'null': 'True', 'blank': 'True'}),
            'birth': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'death': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'diplomacy': ('django.db.models.fields.PositiveIntegerField', [], {'default': '7'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'father': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['kingdom.Folk']"}),
            'fight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '7'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kingdom.Kingdom']", 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'loyalty': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'mentor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['kingdom.Folk']"}),
            'mother': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['kingdom.Folk']"}),
            'plot': ('django.db.models.fields.PositiveIntegerField', [], {'default': '7'}),
            'quality_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['kingdom.Quality']", 'null': 'True', 'blank': 'True'}),
            'scholarship': ('django.db.models.fields.PositiveIntegerField', [], {'default': '7'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'spouse': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['kingdom.Folk']"})
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
        u'kingdom.message': {
            'Meta': {'object_name': 'Message'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kingdom.Kingdom']"}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'read': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'kingdom.modalmessage': {
            'Meta': {'object_name': 'ModalMessage'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kingdom.Kingdom']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
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

    complete_apps = ['kingdom']