# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models


class News(models.Model):
    content = models.TextField(verbose_name=u"Содержание")
    dt = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания")

    def __unicode__(self): return self.content

    class Meta:
        verbose_name = u"Админская новость"
        verbose_name_plural = u"Админские новости"
        ordering = ('-dt',)


class CommonNews(models.Model):
    author = models.ForeignKey(User, verbose_name=u"Автор")
    title = models.CharField(verbose_name=u"Заголовок", max_length=100)
    content = models.TextField(verbose_name=u"Содержание")
    dt = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания")

    def __unicode__(self): return self.title

    class Meta:
        verbose_name = u"Новость"
        verbose_name_plural = u"Новости"
        ordering = ('-dt',)