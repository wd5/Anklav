# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'is_staff', 'is_superuser', 'change_user_link'
        )


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'name', 'user_username', 'user_email',
        'tel', 'city', 'role',
        'role_locked', 'profile_link', 'form_link'
    )
    list_per_page = 300

    def lookup_allowed(self, *args, **kwargs):
            return True


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'profession', 'profile')
    raw_id_fields = ('profile',)


class RoleConnectionAdmin(admin.ModelAdmin):
    list_display = ('role', 'role_rel', 'is_locked')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(RoleConnection, RoleConnectionAdmin)

admin.site.register(Tradition)
admin.site.register(TraditionGuestbook)
admin.site.register(TraditionText)