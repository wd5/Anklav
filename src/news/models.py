# -*- coding: utf-8 -*-

from django.db import models


class News(models.Model):
    content = models.TextField(verbose_name=u"Содержание")
    dt = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания")

    def __unicode__(self): return self.content

    class Meta:
        verbose_name = u"Новость"
        verbose_name_plural = u"Новости"
        ordering = ('-dt',)