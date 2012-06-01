# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from yafotki.fields import YFField


class Article(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, default=None)
    title = models.CharField(verbose_name=u"Заголовок", max_length=50)
    content = models.TextField(verbose_name=u"Содержание")
    order = models.PositiveSmallIntegerField(verbose_name=u"Порядок", default=100)

    def __unicode__(self): return self.title

    class Meta:
        verbose_name = u"Страница"
        verbose_name_plural = u"Страницы"
        ordering = ('order',)