# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.forms import *
from django.db.models import Q

from models import *


class CommonForm(Form):
    def errors_list(self):
        return [u"%s: %s" % (self.fields[_].label, message) for _, l in self.errors.items() for message in l]

    def str_errors(self, divider=u" "):
        return divider.join(self.errors_list())


class RegistrationForm(CommonForm):
    login = CharField(label=u'Ник', max_length=100)
    passwd = CharField(label=u'Пароль', max_length=100, widget=PasswordInput)
    email = EmailField(label=u'Email', max_length=100)
    name = CharField(label=u'ФИО', max_length=100)
    age = IntegerField(label=u'Возраст')
    city = CharField(label=u'Город', max_length=100)
    icq = IntegerField(label=u'ICQ')
    tel = CharField(label=u'Телефон', max_length=100, required=False)
    med = CharField(label=u'Мед. особенности', max_length=100, widget=Textarea, required=False)
    portrait = ImageField(label=u'Фото')

    def clean_login(self):
        try:
            User.objects.get(username=self.cleaned_data['login'])
            raise ValidationError(u"Этот ник занят. Может, вы уже зарегистрированы на сайте?")
        except User.DoesNotExist:
            return self.cleaned_data['login']

    def save(self):
        new_user = User.objects.create_user(self.cleaned_data['login'],
            self.cleaned_data['email'],
            self.cleaned_data['passwd'])
        new_user.is_active = True
        new_user.save()

        profile = Profile.objects.create(
            user=new_user,
            name=self.cleaned_data['name'],
            age=self.cleaned_data['age'],
            city=self.cleaned_data['city'],
            icq=self.cleaned_data['icq'],
            tel=self.cleaned_data['tel'],
            med=self.cleaned_data['med'],
            portrait=self.cleaned_data['portrait'],
        )

        return authenticate(username=new_user.username, password=self.cleaned_data['passwd'])


class ChooseRoleForm(CommonForm):
    role = IntegerField(label=u'Роль', widget=Select)

    def __init__(self, *args, **kwargs):
        super(ChooseRoleForm, self).__init__(*args, **kwargs)
        self.fields['role'].widget.choices = ((role.pk, role.name) for role in Role.objects.filter(profile__isnull=True).order_by('name'))

    def clean_role(self):
        try:
            return Role.objects.get(pk=self.cleaned_data['role'], profile__isnull=True)
        except Role.DoesNotExist:
            raise ValidationError(u"Эта роль занята, попробуйте выбрать другую")


class TraditionTextForm(CommonForm):
    title = CharField(label=u'Название', max_length=100)
    content = CharField(label=u"Содержание", widget=Textarea)


from django.forms.models import modelform_factory, inlineformset_factory
ProfileForm = modelform_factory(Profile, exclude=('user', 'role', 'paid', 'locked_fields'))
RoleForm = modelform_factory(Role, exclude=('order', 'profile', 'quest', 'special'))
QuestForm = modelform_factory(Role, fields=('quest',))
TraditionForm = modelform_factory(Tradition, fields=('content',))
TraditionTextModelForm = modelform_factory(TraditionText, fields=('title', 'content',))
ConnectionFormSet = inlineformset_factory(Role, RoleConnection, fk_name="role", exclude=('is_locked',), extra=1)
#LayerFormSet = inlineformset_factory(Role, LayerConnection, fk_name="role", exclude=('is_locked',), extra=1)