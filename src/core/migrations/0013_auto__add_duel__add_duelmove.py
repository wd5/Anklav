# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Duel'
        db.create_table('core_duel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='role_1', to=orm['core.Role'])),
            ('role_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='role_2', to=orm['core.Role'])),
            ('state', self.gf('django.db.models.fields.CharField')(default='not_started', max_length=20)),
            ('number_1', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('number_2', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='winner', to=orm['core.Role'])),
        ))
        db.send_create_signal('core', ['Duel'])

        # Adding model 'DuelMove'
        db.create_table('core_duelmove', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('duel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Duel'])),
            ('dt', self.gf('django.db.models.fields.DateTimeField')(default=None)),
            ('move_1', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True, blank=True)),
            ('result_1', self.gf('django.db.models.fields.CharField')(default=None, max_length=4, null=True, blank=True)),
            ('move_2', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True, blank=True)),
            ('result_2', self.gf('django.db.models.fields.CharField')(default=None, max_length=4, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['DuelMove'])


    def backwards(self, orm):
        # Deleting model 'Duel'
        db.delete_table('core_duel')

        # Deleting model 'DuelMove'
        db.delete_table('core_duelmove')


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
        'core.duel': {
            'Meta': {'object_name': 'Duel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_1': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'number_2': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'role_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'role_1'", 'to': "orm['core.Role']"}),
            'role_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'role_2'", 'to': "orm['core.Role']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'not_started'", 'max_length': '20'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'winner'", 'to': "orm['core.Role']"})
        },
        'core.duelmove': {
            'Meta': {'object_name': 'DuelMove'},
            'dt': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'duel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Duel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'move_1': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'move_2': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'result_1': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'result_2': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '4', 'null': 'True', 'blank': 'True'})
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
            'corporation': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'corporation'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Tradition']"}),
            'crime': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'crime'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Tradition']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'money': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10000'}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locked_role'", 'null': 'True', 'to': "orm['core.Profile']"}),
            'quest': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'special': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'tradition': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'tradition'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Tradition']"}),
            'work': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.roleconnection': {
            'Meta': {'object_name': 'RoleConnection'},
            'comment': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': "orm['core.Role']"}),
            'role_rel': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'linked_roles'", 'null': 'True', 'to': "orm['core.Role']"})
        },
        'core.tradition': {
            'Meta': {'object_name': 'Tradition'},
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'master'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Role']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'tradition'", 'max_length': '15'})
        },
        'core.traditionguestbook': {
            'Meta': {'object_name': 'TraditionGuestbook'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'dt_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tradition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tradition']"})
        },
        'core.traditiontext': {
            'Meta': {'object_name': 'TraditionText'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'dt_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tradition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tradition']"})
        }
    }

    complete_apps = ['core']