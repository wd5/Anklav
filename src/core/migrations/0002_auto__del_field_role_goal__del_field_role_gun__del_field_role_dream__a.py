# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Role.goal'
        db.delete_column('core_role', 'goal')

        # Deleting field 'Role.gun'
        db.delete_column('core_role', 'gun')

        # Deleting field 'Role.dream'
        db.delete_column('core_role', 'dream')

        # Adding field 'Role.age'
        db.add_column('core_role', 'age',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Role.location'
        db.add_column('core_role', 'location',
                      self.gf('django.db.models.fields.CharField')(default='anklav', max_length=20),
                      keep_default=False)

        # Adding field 'Role.tradition'
        db.add_column('core_role', 'tradition',
                      self.gf('django.db.models.fields.CharField')(default='unknown', max_length=20),
                      keep_default=False)

        # Adding field 'Role.work'
        db.add_column('core_role', 'work',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Role.money'
        db.add_column('core_role', 'money',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Role.quest'
        db.add_column('core_role', 'quest',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Role.goal'
        db.add_column('core_role', 'goal',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Role.gun'
        db.add_column('core_role', 'gun',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Role.dream'
        db.add_column('core_role', 'dream',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Role.age'
        db.delete_column('core_role', 'age')

        # Deleting field 'Role.location'
        db.delete_column('core_role', 'location')

        # Deleting field 'Role.tradition'
        db.delete_column('core_role', 'tradition')

        # Deleting field 'Role.work'
        db.delete_column('core_role', 'work')

        # Deleting field 'Role.money'
        db.delete_column('core_role', 'money')

        # Deleting field 'Role.quest'
        db.delete_column('core_role', 'quest')


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
        'core.profile': {
            'Meta': {'object_name': 'Profile'},
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'icq': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked_fields': ('django.db.models.fields.CharField', [], {'max_length': "'300'", 'null': 'True', 'blank': 'True'}),
            'med': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'portrait': ('yafotki.fields.YFField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'suggested_role'", 'null': 'True', 'to': "orm['core.Role']"}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'core.role': {
            'Meta': {'ordering': "('order', 'name')", 'object_name': 'Role'},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'money': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10000'}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locked_role'", 'null': 'True', 'to': "orm['core.Profile']"}),
            'quest': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'special': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'tradition': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'work': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.roleconnection': {
            'Meta': {'object_name': 'RoleConnection'},
            'comment': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': "orm['core.Role']"}),
            'role_rel': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'linked_roles'", 'null': 'True', 'to': "orm['core.Role']"})
        }
    }

    complete_apps = ['core']