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
    list_display = ('name', 'profession', 'profile', 'dd_number')
    raw_id_fields = ('profile',)


class RoleConnectionAdmin(admin.ModelAdmin):
    list_display = ('role', 'role_rel', 'is_locked')


class TraditionRoleAdmin(admin.ModelAdmin):
    list_display = ('tradition', 'role', 'level', 'is_approved')
    list_filter = ('level', 'is_approved', 'tradition')


class TraditionTextAdmin(admin.ModelAdmin):
    list_display = ('tradition', 'author', 'title')
    list_filter = ('tradition',)


class TraditionFileAdmin(admin.ModelAdmin):
    list_display = ('tradition', 'author', 'title')
    list_filter = ('tradition',)


class RoleMiracleAdmin(admin.ModelAdmin):
    list_display = ('owner', 'miracle', 'recipient')


class DuelMoveInline(admin.TabularInline):
    model = DuelMove
    fk_name = 'duel'
    extra = 0

class DuelAdmin(admin.ModelAdmin):
    list_display = ('role_1', 'role_2', 'state', 'winner', 'result')
    inlines = (DuelMoveInline,)


class HackMoveInline(admin.TabularInline):
    model = HackMove
    fk_name = 'hack'
    extra = 0

class HackAdmin(admin.ModelAdmin):
    list_display = ('hacker', 'key', 'number', 'result')
    inlines = (HackMoveInline,)

class TraditionHackMoveInline(admin.TabularInline):
    model = TraditionHackMove
    fk_name = 'hack'
    extra = 0

class TraditionHackAdmin(admin.ModelAdmin):
    list_display = ('hacker', 'key', 'result')
    inlines = (TraditionHackMoveInline,)



class RoleStockAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'amount')
    list_filter = ('role', 'company')


class DealAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'amount', 'cost', 'buyer', 'is_closed')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(RoleConnection, RoleConnectionAdmin)

admin.site.register(Tradition)
admin.site.register(TraditionGuestbook)
admin.site.register(TraditionText, TraditionTextAdmin)
admin.site.register(TraditionFile, TraditionTextAdmin)
admin.site.register(TraditionRole, TraditionRoleAdmin)

admin.site.register(Miracle)
admin.site.register(RoleMiracle, RoleMiracleAdmin)

admin.site.register(Hack, HackAdmin)
admin.site.register(TraditionHack, TraditionHackAdmin)
admin.site.register(Duel, DuelAdmin)

admin.site.register(DDRequest)
admin.site.register(DDMessage)

admin.site.register(RoleStock, RoleStockAdmin)
admin.site.register(Deal, DealAdmin)
