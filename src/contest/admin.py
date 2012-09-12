# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

class ContestVoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'member')
    list_filter = ('member',)

admin.site.register(ContestMember)
admin.site.register(ContestVote, ContestVoteAdmin)