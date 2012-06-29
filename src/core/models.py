# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from yafotki.fields import YFField


class Role(models.Model):
    name = models.CharField(max_length=200, verbose_name=u"ФИО персонажа")
    age = models.PositiveIntegerField(verbose_name=u"Возраст персонажа")
    LOCATIONS = (
        ('corporation', u'Сотрудник корпорации'),
        ('anklav', u'Житель анклава'),
        ('guest', u'Гость анклава'),
        ('world', u'Внешний мир'),
    )
    location = models.CharField(choices=LOCATIONS, max_length=20, verbose_name=u"Локация")
    tradition = models.ForeignKey('Tradition', verbose_name=u"Традиция", null=True, blank=True, default=None,
        related_name='tradition', limit_choices_to={'type': 'tradition'})
    corporation = models.ForeignKey('Tradition', verbose_name=u"Корпорация", null=True, blank=True, default=None,
        related_name='corporation', limit_choices_to={'type': 'corporation'})
    crime = models.ForeignKey('Tradition', verbose_name=u"Криминал", null=True, blank=True, default=None,
        related_name='crime', limit_choices_to={'type': 'crime'})
    work = models.CharField(max_length=200, verbose_name=u"Место работы")
    profession = models.CharField(max_length=200, verbose_name=u"Специальность")
    description = models.TextField(verbose_name=u"Общеизвестная информация", null=True, blank=True)
    special = models.TextField(verbose_name=u'Спец. способности', null=True, blank=True, default=None)
    money = models.PositiveIntegerField(verbose_name=u"Деньги", null=True, blank=True, default=None)
    quest = models.TextField(verbose_name=u"Квента", null=True, blank=True)

    order = models.IntegerField(verbose_name=u"Порядок", default=10000)
    profile = models.ForeignKey('Profile', verbose_name=u'Профиль', null=True, blank=True, related_name="locked_role")

    def __unicode__(self):
        return self.name


    def save(self, check_diff=True, *args, **kwargs):
        if check_diff:
            report = ""
            if self.pk:
                prev = self.__class__.objects.get(pk=self.pk)
                header = u"Измененные поля роли %s\n" % self.name
                for field in self._meta.fields:
                    if field.name in ('order', 'profile'):
                        continue

                    if getattr(self, field.name) != getattr(prev, field.name):
                        report += u"%s: '%s' -> '%s'\n" % (field.verbose_name, getattr(prev, field.name) or '-', getattr(self, field.name) or '-')
            else:
                header = u"Новая роль %s:\n" % self.name
                for field in self._meta.fields:
                    if field.name in ('order', 'profile'):
                        continue
                    report += u"%s: '%s'\n" % (field.verbose_name, getattr(self, field.name) or '-')

            if report:
                emails = [settings.MANAGERS[0][1], settings.ADMINS[0][1]]
                if self.profile:
                    emails.append(self.profile.user.email)

                send_mail(
                    u"Аклав: роль %s" % self.name,
                    header + report,
                    settings.SERVER_EMAIL,
                    emails,
                    fail_silently=True,
                )

        return super(Role, self).save(*args, **kwargs)


    class Meta:
        verbose_name = u"Роль"
        verbose_name_plural = u"Роли"
        ordering = ('order', 'name',)


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Пользователь', null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name=u"ФИО", null=True, blank=True)
    age = models.IntegerField(verbose_name=u"Возраст", null=True, blank=True)
    city = models.CharField(max_length=200, verbose_name=u"Город", null=True, blank=True)
    icq = models.CharField(max_length=200, verbose_name=u"ICQ", null=True, blank=True)
    tel = models.CharField(max_length=200, verbose_name=u"Телефон", null=True, blank=True)
    med = models.CharField(max_length=200, verbose_name=u"Медицинские особенности", null=True, blank=True)
    portrait = YFField(
        verbose_name=u"Фото",
        upload_to='anklav',
        null=True, blank=True, default=None,
    )

    role = models.ForeignKey(Role, verbose_name=u"Роль", null=True, blank=True, related_name="suggested_role")
    paid = models.BooleanField(verbose_name=u"Взнос внесен", default=False)

    locked_fields = models.CharField(max_length="300", verbose_name=u"Замороженные поля", null=True, blank=True)

    def __unicode__(self):
        return self.name or ""

    def form_link(self):
        return "<a href='" + reverse('form') + '?change_user=%s' % self.user.id + "'>роль</a>"
    form_link.short_description = u"Роль"
    form_link.allow_tags = True

    def profile_link(self):
        return "<a href='" + reverse('profile') + '?change_user=%s' % self.user.id + "'>профиль</a>"
    profile_link.short_description = u"Профиль"
    profile_link.allow_tags = True

    def user_email(self):
        return self.user.email
    user_email.short_description = u"Email"

    def user_username(self):
        return self.user.username
    user_username.short_description = u"Ник"

    def role_locked(self):
        if not self.role:
            return ''
        return self.role.profile == self and '+' or ''
    role_locked.short_description = u"Роль заморожена"

    def is_locked(self, field):
        return self.locked_fields and field in self.locked_fields

    def lock(self, field):
        if not self.locked_fields:
            self.locked_fields = ''
        if not self.is_locked(field):
            fields = self.locked_fields.split(',')
            fields.append(field)
            self.locked_fields = ",".join(fields)
            self.save()

            if field == 'role':
                self.role.profile = self
                self.role.save()

    def unlock(self, field):
        if not self.locked_fields:
            self.locked_fields = ''
        if self.is_locked(field):
            fields = self.locked_fields.split(',')
            fields.append(field)
            self.locked_fields = ",".join([f for f in fields if f != field])
            self.save()

            if field == 'role':
                self.role.profile = None
                self.role.save()


    def save(self, check_diff=True, *args, **kwargs):
        if check_diff:
            report = ""
            if self.pk:
                prev = self.__class__.objects.get(pk=self.pk)
                report = u"Измененные поля профиля [http://anklav-ekb.ru/profile?change_user=%s]:\n" % self.user.pk
                for field in self._meta.fields:
                    if field.name in('paid', 'locked_fields'):
                        continue

                    if getattr(self, field.name) != getattr(prev, field.name):
                        report += u"%s: '%s' -> '%s'\n" % (field.verbose_name, getattr(prev, field.name) or '-', getattr(self, field.name) or '-')
            else:
                report = u"Новый игрок [http://anklav-ekb.ru/profile?change_user=%s]:\n" % self.user.pk
                for field in self._meta.fields:
                    if field.name in('paid', 'locked_fields'):
                        continue
                    report += u"%s: '%s'\n" % (field.verbose_name, getattr(self, field.name) or '-')

            if report:
                emails = [settings.MANAGERS[0][1], settings.ADMINS[0][1], self.user.email]

                send_mail(
                    u"Аклав: профиль игрока %s" % self.name,
                    report,
                    settings.SERVER_EMAIL,
                    emails,
                    fail_silently=True,
                )

        return super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Профиль"
        verbose_name_plural = u"Профили"


class RoleConnection(models.Model):
    role = models.ForeignKey(Role, verbose_name=u"Роль", related_name='roles')
    role_rel = models.ForeignKey(Role, verbose_name=u"Связанная роль", related_name='linked_roles', null=True, blank=True)
    comment = models.TextField(verbose_name=u"Описание", null=True, blank=True, default=None)
    is_locked = models.BooleanField(verbose_name=u"Заморожено", default=False)

    def save(self, *args, **kwargs):
        emails = [settings.MANAGERS[0][1], settings.ADMINS[0][1]]
        if self.role.profile:
            emails.append(self.role.profile.user.email)

        if self.pk:
            prev = self.__class__.objects.get(pk=self.pk)
            if getattr(self, 'comment') != getattr(prev, 'comment'):
                report = u"Анкета: http://anklav-ekb.ru/form?change_user=%s\n\nИзмененная связь: %s -> %s:\nБыло: %s\nСтало: '%s'" %\
                         (self.role.profile.user.pk, self.role,
                          self.role_rel, getattr(prev, 'comment') or '-', getattr(self, 'comment') or '-')

                send_mail(
                    u"Анклав: изменения в связях роли %s" % self.role,
                    report,
                    settings.SERVER_EMAIL,
                    emails,
                    fail_silently=True,
                )
        else:
            if self.role.profile:
                profile = self.role.profile
            else:
                profile = Profile.objects.filter(role=self.role)[0]

            send_mail(
                u"Анклав: новая связь между ролями",
                u"Анкета: http://anklav-ekb.ru/form?change_user=%s\n\n%s -> %s\n\n%s"
                % (profile.user.pk, self.role, self.role_rel, self.comment),
                settings.SERVER_EMAIL,
                emails,
                fail_silently=True,
            )

        return super(RoleConnection, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Связь ролей"
        verbose_name_plural = u"Связи ролей"


class Tradition(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"Название")
    code = models.CharField(max_length=50, verbose_name=u"Код", help_text=u"Англ. строчные буквы без пробелов", default="")
    content = models.TextField(verbose_name=u"Описание", default="")
    master = models.ForeignKey(Role, verbose_name=u"Иерарх", related_name="master", null=True, blank=True, default=None)
    TYPES = (
        ('corporation', u'Корпорация'),
        ('tradition', u'Традиция'),
        ('crime', u'Преступная группировка'),
        )
    type = models.CharField(verbose_name=u"Тип компании", default='tradition', max_length=15, choices=TYPES)

    def __unicode__(self):
        return u"%s '%s'" % (self.get_type_display(), self.name)

    class Meta:
        verbose_name = u"Компания"
        verbose_name_plural = u"Компании"


class TraditionGuestbook(models.Model):
    tradition = models.ForeignKey(Tradition, verbose_name=u"Компания")
    author = models.ForeignKey(User, verbose_name=u"Юзер")
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Добавлено")
    content = models.TextField(verbose_name=u"Содержимое")

    class Meta:
        verbose_name = u"Запись в Компании"
        verbose_name_plural = u"Записи в Компаниях"


class TraditionText(models.Model):
    tradition = models.ForeignKey(Tradition, verbose_name=u"Компания")
    author = models.ForeignKey(User, verbose_name=u"Юзер")
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Добавлено")
    title = models.CharField(max_length=50, verbose_name=u"Название")
    content = models.TextField(verbose_name=u"Содержимое")

    class Meta:
        verbose_name = u"Текст в Компании"
        verbose_name_plural = u"Тексты в Компаниях"


def change_user_link(self):
    return "<a href='" + reverse('change_user', args=[self.id]) + "'>сменить пользователя</a>"
change_user_link.short_description = u"Сменить пользователя"
change_user_link.allow_tags = True

User.change_user_link = change_user_link