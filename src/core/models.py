# -*- coding: utf-8 -*-
import uuid
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from .utils import email
from yafotki.fields import YFField
from BeautifulSoup import BeautifulSoup, Comment as HtmlComment


def sanitizeHTML(value, mode='none'):
    """ Удаляет из value html-теги.
        Если mode==none - все теги
        Если mode==strict - все теги кроме разрешенных
    """
    if mode == 'strict':
        valid_tags = 'ol ul li p i strong b u a h1 h2 h3 pre br div span img blockquote glader youtube cut blue object param embed iframe'.split()
    else:
        valid_tags = []
    valid_attrs = 'href src pic user page class text title alt'.split()
    # параметры видеороликов
    valid_attrs += 'width height classid codebase id name value flashvars allowfullscreen allowscriptaccess quality src type bgcolor base seamlesstabbing swLiveConnect pluginspage data frameborder'.split()

    soup = BeautifulSoup(value)
    for comment in soup.findAll(
        text=lambda text: isinstance(text, HtmlComment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        tag.attrs = [(attr, val) for attr, val in tag.attrs
                                 if attr in valid_attrs]
    result = soup.renderContents().decode('utf8')
    return result


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
    work = models.CharField(max_length=200, verbose_name=u"Место работы")
    profession = models.CharField(max_length=200, verbose_name=u"Специальность")
    description = models.TextField(verbose_name=u"Общеизвестная информация", null=True, blank=True)
    special = models.TextField(verbose_name=u'Спец. способности', null=True, blank=True, default=None)
    money = models.PositiveIntegerField(verbose_name=u"Деньги", default=0)
    quest = models.TextField(verbose_name=u"Квента", null=True, blank=True)
    defender = models.ForeignKey('self', verbose_name=u"Защитник", null=True, blank=True, default=None, related_name='role_security')
    online = models.BooleanField(verbose_name=u"Подключен к сети", default=True)

    dd_number = models.PositiveIntegerField(verbose_name=u"DD", null=True, blank=True, default=None)

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

                email(
                    u"Анклав: роль %s" % self.name,
                    header + report,
                    [],
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
        return self.role.profile == self \
               and '<a href="/lock_role/%s" title="Разморозить">+</a>' % self.user_id \
               or '<a href="/lock_role/%s" title="Заморозить">-</a>' % self.user_id
    role_locked.short_description = u"Роль заморожена"
    role_locked.allow_tags = True

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
                emails = [self.user.email]

                email(
                    u"Анклав: профиль игрока %s" % self.name,
                    report,
                    emails,
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

                email(
                    u"Анклав: изменения в связях роли %s" % self.role,
                    report,
                    emails,
                )
        else:
            if self.role.profile:
                profile = self.role.profile
            else:
                profile = Profile.objects.filter(role=self.role)[0]

            email(
                u"Анклав: новая связь между ролями",
                u"Анкета: http://anklav-ekb.ru/form?change_user=%s\n\n%s -> %s\n\n%s"
                % (profile.user.pk, self.role, self.role_rel, self.comment),
                emails,
            )

        return super(RoleConnection, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Связь ролей"
        verbose_name_plural = u"Связи ролей"


class Tradition(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"Название")
    code = models.CharField(max_length=50, verbose_name=u"Код", help_text=u"Англ. строчные буквы без пробелов", default="")
    content = models.TextField(verbose_name=u"Описание", default="")
    TYPES = (
        ('corporation', u'Корпорация'),
        ('tradition', u'Традиция'),
        ('crime', u'Преступная группировка'),
        )
    type = models.CharField(verbose_name=u"Тип компании", default='tradition', max_length=15, choices=TYPES)
    mana = models.IntegerField(verbose_name=u"Мана", default=0)

    def __unicode__(self):
        return u"%s '%s'" % (self.get_type_display(), self.name)

    def membership(self, role):
        try:
            return TraditionRole.objects.get(role=role, tradition=self)
        except TraditionRole.DoesNotExist:
            return None

    class Meta:
        verbose_name = u"Компания"
        verbose_name_plural = u"Компании"


class TraditionGuestbook(models.Model):
    tradition = models.ForeignKey(Tradition, verbose_name=u"Компания")
    author = models.ForeignKey(User, verbose_name=u"Юзер")
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Добавлено")
    content = models.TextField(verbose_name=u"Содержимое")

    def save(self, *args, **kwargs):
        self.content = sanitizeHTML(self.content)
        super(TraditionGuestbook, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Запись в Компании"
        verbose_name_plural = u"Записи в Компаниях"


class TraditionText(models.Model):
    tradition = models.ForeignKey(Tradition, verbose_name=u"Компания")
    author = models.ForeignKey(User, verbose_name=u"Юзер")
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Добавлено")
    title = models.CharField(max_length=50, verbose_name=u"Название")
    content = models.TextField(verbose_name=u"Содержимое")

    def __unicode__(self):
        return u"%s: %s" % (self.tradition, self.title)

    def save(self, *args, **kwargs):
        self.content = sanitizeHTML(self.content, mode='strict')
        super(TraditionText, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Текст в Компании"
        verbose_name_plural = u"Тексты в Компаниях"


class TraditionFile(models.Model):
    tradition = models.ForeignKey(Tradition, verbose_name=u"Компания")
    author = models.ForeignKey(User, verbose_name=u"Юзер")
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name=u"Добавлено")
    title = models.CharField(max_length=50, verbose_name=u"Название")
    file = models.FileField(upload_to='files', verbose_name=u"Файл")

    class Meta:
        verbose_name = u"Файл в Компании"
        verbose_name_plural = u"Файлы в Компаниях"


class TraditionRole(models.Model):
    tradition = models.ForeignKey(Tradition, verbose_name=u"Компания")
    role = models.ForeignKey(Role, verbose_name=u"Роль")
    is_approved = models.BooleanField(verbose_name=u"Подтверждена", default=False)
    LEVELS = (
        ('ordinal', u"Рядовой"),
        ('security', u"Машинист"),
        ('economy', u"Экономист"),
        ('media', u"Пресс-аналитик"),
        ('master', u"Иерарх"),
    )
    level = models.CharField(choices=LEVELS, max_length=15, verbose_name=u"Должность", default='ordinal')

    class Meta:
        verbose_name = u"Роль в Компании"
        verbose_name_plural = u"Роли в Компаниях"


class Miracle(models.Model):
    name = models.CharField(verbose_name=u"Название", max_length=100)
    description = models.CharField(verbose_name=u"Описание", max_length=250, default="", blank=True)
    cost = models.PositiveIntegerField(verbose_name=u"Сколько маны стоит")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Чудо"
        verbose_name_plural = u"Чудеса"


class RoleMiracle(models.Model):
    owner = models.ForeignKey(Role, verbose_name=u"Владелец чуда", related_name='owner')
    miracle = models.ForeignKey(Miracle, verbose_name=u"Чудо")
    recipient = models.ForeignKey(Role, verbose_name=u"На кого применено", null=True, blank=True, default=None, related_name='recipient')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u"Выдано")
    use_dt = models.DateTimeField(verbose_name=u"Использовано", null=True, blank=True, default=None)

    def __unicode__(self):
        return u"%s: %s" % (self.owner, self.miracle)

    class Meta:
        verbose_name = u"Подаренное чудо"
        verbose_name_plural = u"Чудеса подаренные"


class Duel(models.Model):
    role_1 = models.ForeignKey(Role, verbose_name=u"Игрок 1", related_name="role_1")
    role_2 = models.ForeignKey(Role, verbose_name=u"Игрок 2", related_name="role_2")
    STATES = (
        ('not_started', u"Не началась"),
        ('in_progress', u"Идет"),
        ('finished', u"завершена"),
    )
    state = models.CharField(verbose_name=u"Состояние", max_length=20, default="not_started", choices=STATES)
    number_1 = models.CharField(verbose_name=u"Загаданное число 1", max_length=10, help_text=u"До 10 символов. Обычно - 4. Машинист должен будет ввести число такой же длины.")
    number_2 = models.CharField(verbose_name=u"Загаданное число 2", max_length=10, null=True, blank=True, default=None)
    winner = models.ForeignKey(Role, verbose_name=u"Победитель", related_name="duel_winner", null=True, blank=True, default=None)
    result = models.CharField(verbose_name=u"Итог", max_length=20, null=True, blank=True, default=None)
    dt = models.DateTimeField(verbose_name=u"Начало дуэли", default=None)

    @classmethod
    def get_result(cls, number, move):
        res = []
        good = list(number)
        for i, l in enumerate(move):
            if l == good[i]:
                res.append('1')
            elif l in good:
                res.append('0')

        res.sort(reverse=True)
        return ''.join(res)

    @property
    def number_len(self):
        return len(str(self.number_1))

    class Meta:
            verbose_name = u"Дуэль"
            verbose_name_plural = u"Взломы: дуэли"


class DuelMove(models.Model):
    duel = models.ForeignKey(Duel, verbose_name=u"Дуэль")
    dt = models.DateTimeField(verbose_name=u"Начало хода", default=None)
    move_1 = models.CharField(verbose_name=u"Ход игрока 1", max_length=10, null=True, blank=True, default=None)
    result_1 = models.CharField(verbose_name=u"Результат игрока 1", max_length=10, null=True, blank=True, default=None)
    move_2 = models.CharField(verbose_name=u"Ход игрока 2", max_length=10, null=True, blank=True, default=None)
    result_2 = models.CharField(verbose_name=u"Результат игрока 2", max_length=10, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if self.move_1 and not self.result_1:
            self.result_1 = Duel.get_result(self.duel.number_2, self.move_1)

        if self.move_2 and not self.result_2:
            self.result_2 = Duel.get_result(self.duel.number_1, self.move_2)

        super(DuelMove, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Ход дуэли"
        verbose_name_plural = u"Ходы дуэлей"



def get_hack_target(key):
    if key.startswith('person'):
        return Role.objects.get(pk=int(key.split('/')[1]))
    else:
        return Tradition.objects.get(pk=int(key.split('/')[1]))


def get_hack_field_display(key):
    from .hack import first
    if key.startswith('person'):
        return first(lambda rec: rec[0] == key.split('/')[2], settings.ROLE_FIELDS)[1]
    else:
        return first(lambda rec: rec[0] == key.split('/')[2], settings.TRADITION_FIELDS)[1]


def get_hack_target_value(key):
    target = get_hack_target(key)
    field = key.split('/')[2]

    if key.startswith('person'):
        if field == 'tradition':
            try:
                tradition = TraditionRole.objects.get(role=target, tradition__type='tradition')
                return u"Традиция: %s" % tradition.tradition.name
            except TraditionRole.DoesNotExist:
                return u"Не состоит в традициях."

        if field == 'special':
            miracles = list(RoleMiracle.objects.filter(owner=target))
            result = u"\n".join(u"Чудо: %s" % miracle.miracle.name for miracle in miracles)
            result += u"\nСпецспособности: %s" % (target.special or u"нет")
            return result

        if field == 'actions':
            actions = RoleStock.objects.filter(role=target, amount__gt=0)
            return "\n".join(u"Корпорация %s, акций %s." % (action.company.name, action.amount) for action in actions)\
            or u"Акций нет."

        if field == 'actions_steal':
            actions = RoleStock.objects.filter(role=target, amount__gt=0).exists()
            return actions and u"Вы получаете одну случайную акцию жителя." or u"Здесь нет ни одной акции."

        if field == 'quest':
            return target.quest

        if field == 'criminal':
            try:
                tradition = TraditionRole.objects.get(role=target, tradition__type='crime')
                return u"Криминальная структура: %s" % tradition.tradition.name
            except TraditionRole.DoesNotExist:
                return u"Не состоит в криминальных структурах."

        if field == 'messages':
            from messages.models import Message
            messages = Message.objects.filter(models.Q(sender=target.profile.user)|models.Q(recipient=target.profile.user))
            return u"\n\n".join(
                u"От кого: %s\nКому: %s\n%s" % (message.sender.get_profile().role.name,
                                                message.recipient.get_profile().role.name,
                                                message.body)
                    for message in messages
            ) or u"Сообщений нет."

    else:
        if field == 'document':
            try:
                tradition_file = TraditionFile.objects.get(tradition=target, title=key.split('/')[3])
                return "http://%s%s%s" % (settings.DOMAIN, settings.MEDIA_URL, tradition_file.file.name)
            except TraditionFile.DoesNotExist:
                try:
                    tradition_text = TraditionText.objects.get(tradition=target, title=key.split('/')[3])
                    return tradition_text.content
                except TraditionFile.DoesNotExist:
                    return u"Документ с указанным названием не найден."

        if field == 'documents_list':
            documents = [doc.title for doc in TraditionFile.objects.filter(tradition=target)] +\
                        [doc.title for doc in TraditionText.objects.filter(tradition=target)]
            result = "\n".join(documents)
            return result or u"Документов нет."

        if field == 'tradition_questbook':
            messages = target.traditionguestbook_set.all().order_by('-dt_created')[:20]
            return u"\n\n".join(
                u"От кого: %s\n%s" % (message.author.get_profile().role.name, message.content)
                    for message in messages
            ) or u"Сообщений нет."

        if field == 'corporation_questbook':
            messages = target.traditionguestbook_set.all().order_by('-dt_created')[:20]
            return u"\n\n".join(
                u"От кого: %s\n%s" % (message.author.get_profile().role.name, message.content)
                    for message in messages
            ) or u"Сообщений нет."


class TraditionHack(models.Model):
    hacker = models.ForeignKey(Role, verbose_name=u"Хакер", related_name="hacker")
    security = models.ForeignKey(Role, verbose_name=u"Машинист", related_name="security", null=True, blank=True, default=None)
    key = models.CharField(max_length=250, verbose_name=u"Цель атаки", help_text=u"Цифра - номер роли или традиции")
    STATES = (
        ('not_started', u"Не началась"),
        ('in_progress', u"Идет"),
        ('win', u"Сломал"),
        ('lose', u"Раскрыт"),
        ('late', u"Опоздал"),
        ('run', u"Сбежал"),
        ('fail', u"Облом"),
        )
    state = models.CharField(verbose_name=u"Состояние", max_length=20, default="not_started", choices=STATES)
    hacker_number = models.CharField(verbose_name=u"Загаданное число ломщика", max_length=4, help_text=u"4 цифры.")
    security_number = models.CharField(verbose_name=u"Загаданное число машиниста", max_length=10)
    winner = models.ForeignKey(Role, verbose_name=u"Победитель", related_name="winner", null=True, blank=True, default=None)
    result = models.CharField(verbose_name=u"Итог", max_length=20, null=True, blank=True, default=None)
    dt = models.DateTimeField(verbose_name=u"Начало дуэли", auto_now_add=True)
    uuid = models.CharField(verbose_name=u"UUID", max_length=32)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4().hex

        super(TraditionHack, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('hack_tradition', args=[self.uuid])

    @property
    def is_finished(self):
        return self.state in ('win', 'lose', 'late', 'run', 'fail')

    def get_target(self):
        return get_hack_target(self.key)

    def get_field_display(self):
        return get_hack_field_display(self.key)

    def get_target_value(self):
        return get_hack_target_value(self.key)

    def description(self):
        return u"%s: %s" % (self.get_target(), self.get_field_display())
    description.short_description = u"Описание"

    class Meta:
        verbose_name = u"Взлом традиции"
        verbose_name_plural = u"Взломы традиций"


class TraditionHackMove(models.Model):
    hack = models.ForeignKey(TraditionHack, verbose_name=u"Взлом")
    dt = models.DateTimeField(verbose_name=u"Начало хода", auto_now_add=True)
    hacker_move = models.CharField(verbose_name=u"Ход хакера", max_length=10, null=True, blank=True, default=None)
    hacker_result = models.CharField(verbose_name=u"Результат хакера", max_length=10, null=True, blank=True, default=None)
    security_move = models.CharField(verbose_name=u"Ход машиниста", max_length=10, null=True, blank=True, default=None)
    security_result = models.CharField(verbose_name=u"Результат машиниста", max_length=10, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if self.hacker_move and not self.hacker_result:
            self.hacker_result = Duel.get_result(self.hack.security_number, self.hacker_move)

        if self.security_move and not self.security_result:
            self.security_result = Duel.get_result(self.hack.hacker_number, self.security_move)

        super(TraditionHackMove, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Ход взлома традиции"
        verbose_name_plural = u"Взломы традиций - ходы"


class Hack(models.Model):
    hacker = models.ForeignKey(Role, verbose_name=u"Хакер")
    key = models.CharField(max_length=250, verbose_name=u"Цель атаки", help_text=u"Цифра - номер роли или традиции")
    dt = models.DateTimeField(auto_now_add=True, verbose_name=u"Начало атаки")
    number = models.CharField(max_length=10, verbose_name=u"Взламываемое число")
    RESULTS = (
        (None, u"Идет"),
        ('win', u"Взломано"),
        ('fail', u"Облом"),
        ('late', u"Опоздал"),
        )
    result = models.CharField(verbose_name=u"Итог", choices=RESULTS, max_length=20, null=True, blank=True, default=None)
    uuid = models.CharField(verbose_name=u"UUID", max_length=32)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4().hex

        super(Hack, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('hack_personal', args=[self.uuid])

    def get_target(self):
        return get_hack_target(self.key)

    def get_field_display(self):
        return get_hack_field_display(self.key)

    def get_target_value(self):
        return get_hack_target_value(self.key)

    def description(self):
        return u"%s: %s" % (self.get_target(), self.get_field_display())
    description.short_description = u"Описание"

    class Meta:
        verbose_name = u"Взлом"
        verbose_name_plural = u"Взломы"


class HackMove(models.Model):
    hack = models.ForeignKey(Hack, verbose_name=u"Взлом")
    dt = models.DateTimeField(verbose_name=u"Начало хода", auto_now_add=True, default=None)
    move = models.CharField(verbose_name=u"Ход", max_length=10, null=True, blank=True, default=None)
    result = models.CharField(verbose_name=u"Результат", max_length=10, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if self.move and not self.result:
            self.result = Duel.get_result(self.hack.number, self.move)

        super(HackMove, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Ход взлома"
        verbose_name_plural = u"Ходы взломов"


class DDRequest(models.Model):
    author = models.ForeignKey(User, verbose_name=u"Автор заявки", related_name='request_author')
    dt = models.DateTimeField(verbose_name=u"Дата заявки", auto_now_add=True)
    description = models.TextField(verbose_name=u"Заявка", help_text=u"Краткое публичное описание задания")
    cost = models.TextField(verbose_name=u"Плата", help_text=u"Тип оплаты за задание. Информация, деньги, акции.")
    assignee = models.ForeignKey(User, verbose_name=u"Исполнитель", related_name='assignee', null=True, blank=True, default=None)
    STATUSES = (
        ('created', u"Создано"),
        ('assigned', u"Назначено"),
        ('ready', u"Готово"),
        ('done', u"Подтверждено"),
        ('fail', u"Провалена"),
    )
    status = models.CharField(verbose_name=u"Статус", default='created', max_length=20, choices=STATUSES)

    def send_notification(self, event):
        recievers = []
        if event == 'assigned':
            recievers.append(self.assignee.email)
        else:
            recievers.append(self.author.email)

        message = {
            'comment': u"Новый комментарий к заявке %s. ",
            'assigned': u"Назначен исполнитель к заявке %s. ",
            'ready': u"Заявка %s помечена как исполненная. ",
            'done': u"Заявка %s помечена как подтвержденная. ",
            'fail': u"Заявка %s помечена как проваленная. ",
            }

        email(
            u"Анклав: уведомление с сервера DD",
            message[event] % self.id +
            "http://%s%s" % (settings.DOMAIN, reverse('dd_request', args=[self.id])),
            recievers
        )

    class Meta:
        verbose_name = u"Заявка DD"
        verbose_name_plural = u"DD: заявки"


class DDComment(models.Model):
    request = models.ForeignKey(DDRequest, verbose_name=u"Заявка")
    author = models.ForeignKey(User, verbose_name=u"Автор")
    dt = models.DateTimeField(verbose_name=u"Дата заявки", auto_now_add=True)
    content = models.TextField(verbose_name=u"Комментарий")

    class Meta:
        verbose_name = u"Комментарий к заявке DD"
        verbose_name_plural = u"DD: комментарии"


class DDMessage(models.Model):
    sender = models.ForeignKey(User, verbose_name=u"Автор", related_name='sender')
    recipient = models.ForeignKey(User, verbose_name=u"Получатель", related_name='recipient')
    dt = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата")
    content = models.TextField(verbose_name=u"Сообщение")

    def save(self, *args, **kwargs):
        self.content = sanitizeHTML(self.content)
        super(DDMessage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"DD: личное сообщение"
        verbose_name_plural = u"DD: переписка"


class RoleStock(models.Model):
    role = models.ForeignKey(Role, verbose_name=u"Роль")
    company = models.ForeignKey(Tradition, verbose_name=u"Компания", limit_choices_to={'type': 'corporation'})
    amount = models.IntegerField(verbose_name=u"Количество акций", default=0)

    class Meta:
        verbose_name = u"Акции"
        verbose_name_plural = u"Акции"


class Deal(models.Model):
    role = models.ForeignKey(Role, verbose_name=u"Продавец", related_name='seller')
    company = models.ForeignKey(Tradition, verbose_name=u"Компания", limit_choices_to={'type': 'corporation'})
    amount = models.PositiveIntegerField(verbose_name=u"Количество акций", default=0)
    dt_add = models.DateTimeField(auto_now_add=True, verbose_name=u"Создано")
    cost = models.PositiveIntegerField(verbose_name=u"Стоимость", default=0)
    buyer = models.ForeignKey(Role, verbose_name=u"Покупатель", related_name='buyer', null=True, blank=True, default=None)
    is_closed = models.BooleanField(verbose_name=u"Исполнено", default=False)
    dt_closed = models.DateTimeField(verbose_name=u"Когда исполнено", null=True, blank=True, default=None)

    class Meta:
        verbose_name = u"Сделка по акциям"
        verbose_name_plural = u"Акции: сделки"


def change_user_link(self):
    return "<a href='" + reverse('change_user', args=[self.id]) + "'>сменить пользователя</a>"
change_user_link.short_description = u"Сменить пользователя"
change_user_link.allow_tags = True

User.change_user_link = change_user_link
