# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django import forms
from yafotki.fields import YFField


class ContestMember(models.Model):
    user = models.ForeignKey(User, verbose_name=u"Участник")
    photo = YFField(
        verbose_name=u"Фото",
        upload_to='anklav',
        null=True, blank=True, default=None,
    )
    count = models.PositiveIntegerField(verbose_name=u"Счет", default=0)

    def __unicode__(self):
        return self.user.get_profile().role.name

    class Meta:
        verbose_name = u"Участник"
        verbose_name_plural = u"Участники"


class ContestVote(models.Model):
    author = models.ForeignKey(User, verbose_name=u"Голосующий", related_name='author')
    member = models.ForeignKey(ContestMember, verbose_name=u"За кого", related_name='member')


ContestMemberForm = forms.models.modelform_factory(ContestMember, fields=('photo',))
