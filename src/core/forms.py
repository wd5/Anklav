# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.contrib.auth import authenticate
from django.forms import *
from django.db.models import Q

from models import *
from .utils import email


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
    icq = IntegerField(label=u'ICQ', required=False)
    tel = CharField(label=u'Телефон', max_length=100, required=False)
    med = CharField(label=u'Мед. особенности', max_length=100, widget=Textarea, required=False)
    portrait = ImageField(label=u'Фото', required=False)

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


class CreateDuelForm(ModelForm):
    class Meta:
        model = Duel
        fields = ('role_2', 'number_1')

    @classmethod
    def check_number(cls, number, number_len=None):
        try:
            int(number)
            if number_len:
                if len(number) != number_len:
                    raise ValidationError(u"Загаданное число должно содержать %s цифр" % number_len)
            else:
                if len(number) > 10:
                    raise ValidationError(u"Загаданное число должно содержать не более 10 цифры")

            if len(set(number)) != len(number):
                raise ValidationError(u"Все цифры числа должны быть разными")

            return number

        except ValueError:
            raise ValidationError(u"Введите четырехзначное число")

    def clean_number_1(self):
        return self.check_number(self.cleaned_data['number_1'])

    def save(self, role, *args, **kwargs):
        duel = Duel.objects.create(
            role_1=role,
            role_2=self.cleaned_data['role_2'],
            number_1=self.cleaned_data['number_1'],
            dt=datetime.now()
        )

        email(
            u"Анклав: Дуэль",
            u"%s, вы вызваны на дуэль. http://anklav-ekb.ru%s" % (self.cleaned_data['role_2'].name, reverse('duel', args=[duel.pk])),
            [self.cleaned_data['role_2'].profile.user.email]
        )

        return duel


class DealForm(CommonForm):
    company = IntegerField(label=u'Фирма', widget=Select)
    amount = IntegerField(label=u'Количество акций')
    cost = IntegerField(label=u'Цена сделки')

    def get_actions(self, role):
        return RoleStock.objects.filter(role=role, amount__gt=0)

    def __init__(self, role, *args, **kwargs):
        super(DealForm, self).__init__(*args, **kwargs)

        self.role = role
        self.fields['company'].widget.choices = ((action.company.pk, action.company.name) for action in self.get_actions(role))

    def clean_company(self):
        try:
            return Tradition.objects.get(pk=self.cleaned_data['company'], type='corporation')
        except Tradition.DoesNotExist:
            raise ValidationError(u"Фирма не найдена")

    def clean(self):
        try:
            actions = RoleStock.objects.get(role=self.role, company=self.cleaned_data['company'])
            if actions.amount < self.cleaned_data['amount']:
                raise ValidationError(u"У вас недостаточно акций этой фирмы, уменьшите заявку до %s акций." % actions.amount)

            return self.cleaned_data

        except RoleStock.DoesNotExist:
            raise ValidationError(u"У вас нет акций этой фирмы")

    def save(self):
        actions = RoleStock.objects.get(role=self.role, company=self.cleaned_data['company'])
        actions.amount -= self.cleaned_data['amount']
        actions.save()

        deal = Deal.objects.create(
            role=self.role,
            amount=self.cleaned_data['amount'],
            company=self.cleaned_data['company'],
            cost=self.cleaned_data['cost'],
        )

        return deal


class TransferForm(CommonForm):
    recipient = IntegerField(label=u'Получатель', widget=Select)
    amount = IntegerField(label=u'Сумма')

    def __init__(self, role, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)

        self.sender = role
        self.fields['recipient'].widget.choices = ((role.pk, role.name) for role in Role.objects.filter(profile__isnull=False).exclude(pk=role.id))

    def clean_recipient(self):
        try:
            return Role.objects.get(pk=self.cleaned_data['recipient'])
        except Role.DoesNotExist:
            raise ValidationError(u"Получатель не найден")

    def clean_amount(self):
        if self.sender.money >= int(self.cleaned_data['amount']):
            return int(self.cleaned_data['amount'])
        else:
            raise ValidationError(u"У вас недостаточно средств")

    def save(self):
        self.sender.money -= self.cleaned_data['amount']
        self.sender.save()

        self.cleaned_data['recipient'].money += self.cleaned_data['amount']
        self.cleaned_data['recipient'].save()


class PersonHackTarget(CommonForm):
    role = IntegerField(label=u'Кого ломаем', widget=Select)
    field = CharField(label=u'Что ломаем', widget=Select)
    number = CharField(label=u'Ваше число', help_text=u"4 цифры")

    def __init__(self, role, *args, **kwargs):
        super(PersonHackTarget, self).__init__(*args, **kwargs)

        self.hacker = role
        self.fields['role'].widget.choices = ((role.pk, role.name) for role in Role.objects.filter(profile__isnull=False).exclude(pk=role.id))
        self.fields['field'].widget.choices = [field[:2] for field in settings.ROLE_FIELDS]

    def clean_role(self):
        try:
            return Role.objects.get(pk=self.cleaned_data['role'])
        except Role.DoesNotExist:
            raise ValidationError(u"Жертва не найдена")

    def clean_number(self):
        number = self.cleaned_data['number']
        number_len = 4
        try:
            int(number)
            if len(number) != number_len:
                raise ValidationError(u"Загаданное число должно содержать %s цифр" % number_len)

            if len(set(number)) != len(number):
                raise ValidationError(u"Все цифры числа должны быть разными")

            return number

        except ValueError:
            raise ValidationError(u"Введите четырехзначное число")

    def clean(self):
        self.cleaned_data['key'] = 'person/%s/%s' % (self.cleaned_data['role'].id, self.cleaned_data['field'])

        yesterday = datetime.now() - timedelta(days=1)
        if Hack.objects.filter(hacker=self.hacker, key=self.cleaned_data['key'], dt__gt=yesterday).exists():
            raise ValidationError(u"Вы недавно уже ломали эту информацию. Передохните.")

        return self.cleaned_data

    def save(self):
        # создаем новый взлом
        from .hack import generate_number

        if self.cleaned_data['role'].defender:
            hack = TraditionHack.objects.create(
                hacker=self.hacker,
                key=self.cleaned_data['key'],
                hacker_number=self.cleaned_data['number'],
                security_number=generate_number(self.cleaned_data['key']),
            )

        else:
            hack = Hack.objects.create(
                hacker=self.hacker,
                key=self.cleaned_data['key'],
                number=generate_number(self.cleaned_data['key']),
            )

        return hack


class TraditionHackTarget(CommonForm):
    tradition = IntegerField(label=u'Кого ломаем', widget=Select)
    field = CharField(label=u'Что ломаем', widget=Select)
    file = CharField(label=u'Имя файла', help_text=u"для взлома одного документа", required=False)
    number = CharField(label=u'Ваше число', help_text=u"4 цифры")

    def __init__(self, role, *args, **kwargs):
        super(TraditionHackTarget, self).__init__(*args, **kwargs)

        self.hacker = role
        self.fields['tradition'].widget.choices = ((tradition.pk, tradition.name) for tradition in Tradition.objects.all())
        self.fields['field'].widget.choices = [field[:2] for field in settings.TRADITION_FIELDS]

    def clean_tradition(self):
        try:
            return Tradition.objects.get(pk=self.cleaned_data['tradition'])
        except Tradition.DoesNotExist:
            raise ValidationError(u"Жертва не найдена")

    def clean_number(self):
        number = self.cleaned_data['number']
        number_len = 4
        try:
            int(number)
            if len(number) != number_len:
                raise ValidationError(u"Загаданное число должно содержать %s цифр" % number_len)

            if len(set(number)) != len(number):
                raise ValidationError(u"Все цифры числа должны быть разными")

            return number

        except ValueError:
            raise ValidationError(u"Введите четырехзначное число")

    def clean(self):
        if self.cleaned_data['tradition'].type == 'tradition' and self.cleaned_data['field'] == 'corporation_questbook':
            raise ValidationError(u"Выберите взлом гостевой книги Традиции")

        if self.cleaned_data['tradition'].type in ('corporation', 'crime') and self.cleaned_data['field'] == 'tradition_questbook':
            raise ValidationError(u"Выберите взлом гостевой книги корпорации")

        if self.cleaned_data['field'] == 'document' and not self.cleaned_data['file']:
            raise ValidationError(u"Введите название документа")

        self.cleaned_data['key'] = u'tradition/%s/%s/%s' % \
            (self.cleaned_data['tradition'].id, self.cleaned_data['field'], self.cleaned_data['file'] or '')

        yesterday = datetime.now() - timedelta(days=1)
        if TraditionHack.objects.filter(hacker=self.hacker, key=self.cleaned_data['key'], dt__gt=yesterday).exists():
            raise ValidationError(u"Вы недавно уже ломали эту информацию. Передохните.")

        return self.cleaned_data

    def save(self):
        # создаем новый взлом
        from .hack import generate_number
        hack = TraditionHack.objects.create(
            hacker=self.hacker,
            key=self.cleaned_data['key'],
            hacker_number=self.cleaned_data['number'],
            security_number=generate_number(self.cleaned_data['key']),
        )

        return hack

from django.forms.models import modelform_factory, inlineformset_factory

ProfileForm = modelform_factory(Profile, exclude=('user', 'role', 'paid', 'locked_fields', 'money'))
RoleForm = modelform_factory(Role, exclude=('order', 'profile', 'quest', 'dd_number', 'defender'))
QuestForm = modelform_factory(Role, fields=('quest',))
TraditionForm = modelform_factory(Tradition, fields=('content',))
TraditionTextModelForm = modelform_factory(TraditionText, fields=('title', 'content',))
TraditionFileForm = modelform_factory(TraditionFile, fields=('title' ,'file'))
ConnectionFormSet = inlineformset_factory(Role, RoleConnection, fk_name="role", exclude=('is_locked',), extra=1)
#LayerFormSet = inlineformset_factory(Role, LayerConnection, fk_name="role", exclude=('is_locked',), extra=1)
DDForm = modelform_factory(DDRequest, fields=('description', 'cost'))