# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

class NewsAdmin(admin.ModelAdmin):
    list_display = ('content',)

admin.site.register(News, NewsAdmin)