# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'user_username', 'user_email', 'tel', 'city', 'role', 'role_locked', 'form_link')
    list_per_page = 300

    def lookup_allowed(self, *args, **kwargs):
            return True


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'profession', 'profile')
    raw_id_fields = ('profile',)


class RoleConnectionAdmin(admin.ModelAdmin):
    list_display = ('role', 'role_rel', 'is_locked')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(RoleConnection, RoleConnectionAdmin)