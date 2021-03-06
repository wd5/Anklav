# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Role.can_defend'
        db.add_column('core_role', 'can_defend',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Role.can_defend'
        db.delete_column('core_role', 'can_defend')


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
        'core.ddcomment': {
            'Meta': {'object_name': 'DDComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.DDRequest']"})
        },
        'core.ddmessage': {
            'Meta': {'object_name': 'DDMessage'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipient'", 'to': "orm['auth.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sender'", 'to': "orm['auth.User']"})
        },
        'core.ddrequest': {
            'Meta': {'object_name': 'DDRequest'},
            'assignee': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'assignee'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'request_author'", 'to': "orm['auth.User']"}),
            'cost': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'created'", 'max_length': '20'})
        },
        'core.deal': {
            'Meta': {'object_name': 'Deal'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'buyer'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Role']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tradition']"}),
            'cost': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'dt_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dt_closed': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seller'", 'to': "orm['core.Role']"})
        },
        'core.duel': {
            'Meta': {'object_name': 'Duel'},
            'dt': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_1': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'number_2': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'role_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'role_1'", 'to': "orm['core.Role']"}),
            'role_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'role_2'", 'to': "orm['core.Role']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'not_started'", 'max_length': '20'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'duel_winner'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Role']"})
        },
        'core.duelmove': {
            'Meta': {'object_name': 'DuelMove'},
            'dt': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'duel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Duel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'move_1': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'move_2': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'result_1': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'result_2': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'core.hack': {
            'Meta': {'object_name': 'Hack'},
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hacker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Role']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'result': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'core.hackmove': {
            'Meta': {'object_name': 'HackMove'},
            'dt': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'auto_now_add': 'True', 'blank': 'True'}),
            'hack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Hack']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'move': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'core.miracle': {
            'Meta': {'object_name': 'Miracle'},
            'cost': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'can_defend': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dd_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'money': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10000'}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locked_role'", 'null': 'True', 'to': "orm['core.Profile']"}),
            'quest': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'special': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
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
        'core.rolemiracle': {
            'Meta': {'object_name': 'RoleMiracle'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miracle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Miracle']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': "orm['core.Role']"}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'recipient'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Role']"}),
            'use_dt': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'core.rolestock': {
            'Meta': {'object_name': 'RoleStock'},
            'amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tradition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Role']"})
        },
        'core.tradition': {
            'Meta': {'object_name': 'Tradition'},
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mana': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'tradition'", 'max_length': '15'})
        },
        'core.traditionfile': {
            'Meta': {'object_name': 'TraditionFile'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'dt_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tradition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tradition']"})
        },
        'core.traditionguestbook': {
            'Meta': {'object_name': 'TraditionGuestbook'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'dt_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tradition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Tradition']"})
        },
        'core.traditionhack': {
            'Meta': {'object_name': 'TraditionHack'},
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hacker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hacker'", 'to': "orm['core.Role']"}),
            'hacker_number': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'result': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'security'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Role']"}),
            'security_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'not_started'", 'max_length': '20'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'winner'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Role']"})
        },
        'core.traditionhackmove': {
            'Meta': {'object_name': 'TraditionHackMove'},
            'dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hack': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.TraditionHack']"}),
            'hacker_move': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'hacker_result': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'security_move': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'security_result': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'core.traditionrole': {
            'Meta': {'object_name': 'TraditionRole'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.CharField', [], {'default': "'ordinal'", 'max_length': '15'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Role']"}),
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