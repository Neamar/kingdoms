# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AvatarCategory'
        db.delete_table(u'internal_avatarcategory')

        # Deleting field 'Avatar.category'
        db.delete_column(u'internal_avatar', 'category_id')

        # Deleting field 'Avatar.image'
        db.delete_column(u'internal_avatar', 'image')

        # Adding field 'Avatar.fight'
        db.add_column(u'internal_avatar', 'fight',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Avatar.diplomacy'
        db.add_column(u'internal_avatar', 'diplomacy',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Avatar.plot'
        db.add_column(u'internal_avatar', 'plot',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Avatar.scholarship'
        db.add_column(u'internal_avatar', 'scholarship',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Avatar.child'
        db.add_column(u'internal_avatar', 'child',
                      self.gf('django.db.models.fields.files.ImageField')(default=1, max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Avatar.teenager'
        db.add_column(u'internal_avatar', 'teenager',
                      self.gf('django.db.models.fields.files.ImageField')(default=1, max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Avatar.adult'
        db.add_column(u'internal_avatar', 'adult',
                      self.gf('django.db.models.fields.files.ImageField')(default=1, max_length=100),
                      keep_default=False)

        # Adding field 'Avatar.old'
        db.add_column(u'internal_avatar', 'old',
                      self.gf('django.db.models.fields.files.ImageField')(default=1, max_length=100),
                      keep_default=False)

        # Adding M2M table for field qualities on 'Avatar'
        m2m_table_name = db.shorten_name(u'internal_avatar_qualities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('avatar', models.ForeignKey(orm[u'internal.avatar'], null=False)),
            ('quality', models.ForeignKey(orm[u'kingdom.quality'], null=False))
        ))
        db.create_unique(m2m_table_name, ['avatar_id', 'quality_id'])


    def backwards(self, orm):
        # Adding model 'AvatarCategory'
        db.create_table(u'internal_avatarcategory', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal(u'internal', ['AvatarCategory'])

        # Adding field 'Avatar.category'
        db.add_column(u'internal_avatar', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['internal.AvatarCategory']),
                      keep_default=False)

        # Adding field 'Avatar.image'
        db.add_column(u'internal_avatar', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(default=1, max_length=100),
                      keep_default=False)

        # Deleting field 'Avatar.fight'
        db.delete_column(u'internal_avatar', 'fight')

        # Deleting field 'Avatar.diplomacy'
        db.delete_column(u'internal_avatar', 'diplomacy')

        # Deleting field 'Avatar.plot'
        db.delete_column(u'internal_avatar', 'plot')

        # Deleting field 'Avatar.scholarship'
        db.delete_column(u'internal_avatar', 'scholarship')

        # Deleting field 'Avatar.child'
        db.delete_column(u'internal_avatar', 'child')

        # Deleting field 'Avatar.teenager'
        db.delete_column(u'internal_avatar', 'teenager')

        # Deleting field 'Avatar.adult'
        db.delete_column(u'internal_avatar', 'adult')

        # Deleting field 'Avatar.old'
        db.delete_column(u'internal_avatar', 'old')

        # Removing M2M table for field qualities on 'Avatar'
        db.delete_table(db.shorten_name(u'internal_avatar_qualities'))


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
            'adult': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'child': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'blank': 'True'}),
            'diplomacy': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fight': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'plot': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'qualities': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['kingdom.Quality']", 'symmetrical': 'False'}),
            'scholarship': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'teenager': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'blank': 'True'})
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
            'delay': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1440'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'on_fire': ('config.fields.script_field.ScriptField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
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
        u'internal.value': {
            'Meta': {'unique_together': "(('name', 'kingdom'),)", 'object_name': 'Value'},
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