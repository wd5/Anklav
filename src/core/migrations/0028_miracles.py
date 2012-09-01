# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."

        miracles = (
            (1, u'Уточнение места, где происходили те или иные события', u'для вычисления места финального ритуала'),
            (1, u'Одноразовый маячок на человека', u'вешается на человека, делая его уязвимым'),
            (2, u'Найти человека', u'т.е. можно один раз через мастера узнать где сейчас находится человек, на которого был повешан маячок'),
            (3, u'Позвать человека', u'т.е. можно через мастера призвать человека в определенное место'),
            (1, u'Снять маячок', u''),
            (3, u'Боевой транс', u'право нанесения двух ударов в состоянии неуязвимом для окружающих. Не может быть использован 2 и более раз подряд'),
            (1, u'Гадание', u'вопрос мастеру на да/нет'),
            (2, u'Допрос души', u'аналог сыворотки правды, так же как и она не действует на вопросы Традиций'),
            (1, u'Погружение в сон на 5 минут', u''),
            (2, u'Исцеление ран', u'может быть использовано на себя'),
            (2, u'Аура силы', u'неуязвим, пока не совершает агрессивных действий'),
            (3, u'Магический обыск', u'заставляет человека отдать все игровые ценности'),
        )

        for miracle in miracles:
            orm.Miracle.objects.create(
                cost=miracle[0],
                name=miracle[1],
                description=miracle[2],
            )

    def backwards(self, orm):
        "Write your backwards methods here."

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
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'winner'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Role']"})
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
        'core.miracle': {
            'Meta': {'object_name': 'Miracle'},
            'cost': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
            'dd_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miracle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Miracle']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': "orm['core.Role']"}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'recipient'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Role']"})
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
    symmetrical = True
