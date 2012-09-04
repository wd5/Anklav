# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import random

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from .forms import *


def render_to_response(request, template_name, context_dict=None):
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict or {})
    return _render_to_response(template_name, context_instance=context)


def registration(request):
    if request.POST:
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect("/")

    else:
        form = RegistrationForm()

    return render_to_response(request, 'registration.html', {'form': form})


def change_user(request, user_id):
    if not request.user.is_superuser:
        raise Http404()
    request.session['_auth_user_id'] = user_id
    return HttpResponseRedirect('/')


def lock_role(request, user_id):
    if not request.user.is_superuser:
        raise Http404()

    profile = User.objects.get(pk=user_id).get_profile()
    if not profile.role:
        return HttpResponseRedirect('/admin/core/profile/')

    role = profile.role
    if role.profile == profile:
        role.profile = None
        role.save()

    else:
        Profile.objects.filter(role=role).exclude(pk=profile.pk).update(role=None)
        role.profile = profile
        role.save()

    return HttpResponseRedirect('/admin/core/profile/')


@login_required
def form(request):
    if request.POST:
        if request.actual_profile.role:
            valid = True
            forms = {
                'form': RoleForm(request.POST, instance=request.actual_profile.role),
                'quest_form': QuestForm(request.POST, instance=request.actual_profile.role),
                'connections_formset': ConnectionFormSet(request.POST, instance=request.actual_profile.role)
            }
            for name, form in forms.items():
                if form.is_valid():
                    form.save()
                else:
                    valid = False

            if valid:
                return HttpResponseRedirect(reverse('form') + '?save=ok&change_user=%s' % request.actual_user.pk)

            return render_to_response(request, 'form.html', forms)

    else:
        if request.actual_profile.role:
            forms = {
                'form': RoleForm(instance=request.actual_profile.role),
                'quest_form': QuestForm(instance=request.actual_profile.role),
                'connections_formset': ConnectionFormSet(instance=request.actual_profile.role)
            }
            return render_to_response(request, 'form.html', forms)

    free_roles = Role.objects.filter(profile__isnull=True)
    if free_roles:
        form = ChooseRoleForm()
        return render_to_response(request, 'choose_role.html', {'form': form})
    else:
        return add_role(request)


@login_required
def choose_role(request):
    if request.actual_role:
        # За пользователем уже закреплена роль
        return HttpResponseRedirect("/")

    if request.POST:
        form = ChooseRoleForm(request.POST)
        if form.is_valid():
            request.actual_profile.role = form.cleaned_data['role']
            request.actual_profile.save()
            return HttpResponseRedirect(reverse('form') + '?save=ok&change_user=%s' % request.actual_user.pk)

    else:
        form = ChooseRoleForm()

    return render_to_response(request, 'choose_role.html', {'form': form})


@login_required
def add_role(request):
    if request.actual_role:
        # За пользователем уже закреплена роль
        return HttpResponseRedirect("/")

    if request.POST:
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            request.actual_profile.role = role
            request.actual_profile.save()
            return HttpResponseRedirect(reverse('form') + '?save=ok&change_user=%s' % request.actual_user.pk)

    else:
        form = RoleForm()

    return render_to_response(request, 'add_role.html', {'form': form})


def roles(request):
    return render_to_response(request, 'core/role_list.html', {
        'object_list': Role.objects.all().order_by('location', 'name'),
        'amount': Role.objects.filter(profile__isnull=False).count(),
    })


@login_required
def profile(request):
    if request.POST:
        form = ProfileForm(request.POST, instance=request.actual_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile') + '?save=ok&change_user=%s' % request.actual_user.pk)
    else:
        form = ProfileForm(instance=request.actual_profile)

    return render_to_response(request, 'profile.html', {'form': form})


def role_required(func):
    def wrapper(request, *args, **kwargs):
        if request.actual_role or request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return render_to_response(request, 'role_required.html')
    return wrapper


def tradition_required(func):
    def wrapper(request, *args, **kwargs):
        if request.actual_role or request.user.is_superuser:
            try:
                tradition = Tradition.objects.get(code=kwargs['code'])
                if request.user.is_superuser or \
                    TraditionRole.objects.filter(tradition=tradition, role=request.actual_role, is_approved=True).exists():
                        return func(request, *args, **kwargs)

            except Tradition.DoesNotExist:
                pass

        raise Http404
    return wrapper


@login_required
def traditions_request(request):
    traditions = Tradition.objects.all().order_by('type', 'name')
    membership = dict((tr.tradition_id, tr) for tr in TraditionRole.objects.filter(role=request.actual_role))
    for tradition in traditions:
        tradition.membership = membership.get(tradition.id, None)

    traditions = filter(lambda t: t.type != 'crime' or t.membership, traditions)

    return render_to_response(request, 'traditions_request.html', {'traditions': traditions})


@login_required
def tradition_request(request, code):
    tradition = Tradition.objects.get(code=code)
    membership = tradition.membership(request.actual_role)

    if request.POST:
        # заявка на участие в группе
        TraditionRole.objects.filter(role=request.actual_role, tradition__type=tradition.type).delete()
        TraditionRole.objects.create(role=request.actual_role, tradition=tradition)

        try:
            master = TraditionRole.objects.get(tradition=tradition, level='master').role
            send_mail(
                u"Анклав: заявка на участие",
                u"Новая заявка на участие: http://%s%s" % (settings.DOMAIN, reverse('tradition_members', args=[tradition.code])),
                None,
                ['linashyti@gmail.com', 'glader.ru@gmail.com', master.profile.user.email],
            )
        except TraditionRole.DoesNotExist:
            send_mail(
                u"Анклав: заявка на участие",
                u"У %s нет иерарха, некому утверждать заявки." % tradition.name,
                None,
                ['linashyti@gmail.com', 'glader.ru@gmail.com'],
            )
        return HttpResponseRedirect(reverse('tradition_request', args=[tradition.code]))

    return render_to_response(request, 'tradition_request.html', {'tradition': tradition, 'membership': membership})


@tradition_required
def tradition_members(request, code):
    tradition = Tradition.objects.get(code=code)
    membership = tradition.membership(request.actual_role)

    if not ((membership and membership.level == 'master') or request.user.is_superuser):
        raise Http404

    members = TraditionRole.objects.filter(tradition=tradition).exclude(level='master').order_by('is_approved', 'role__name')

    if request.POST:
        try:
            role_id = int(request.POST['role'])
            relation = tradition.membership(Role.objects.get(pk=role_id))
            if request.POST['action'] == u'Принять':
                relation.is_approved = True
                relation.save()
                tradition.mana += TraditionRole.objects.filter(tradition=tradition, is_approved=True).exclude(level='master').count()
                tradition.save()
            else:
                tradition.mana -= TraditionRole.objects.filter(tradition=tradition, is_approved=True).exclude(level='master').count()
                tradition.save()
                relation.delete()
            return HttpResponseRedirect(reverse('tradition_members', args=[tradition.code]))
        except (Role.DoesNotExist, AttributeError, ValueError):
            pass

    return render_to_response(request, 'tradition_members.html', {'tradition': tradition, 'members': members})


@tradition_required
def tradition_miracles(request, code):
    error = ""
    tradition = Tradition.objects.get(code=code)
    if tradition.type != 'tradition':
        raise Http404

    membership = tradition.membership(request.actual_role)
    if not ((membership and membership.level == 'master') or request.user.is_superuser):
        raise Http404

    if request.POST:
        # одаривание чудом
        try:
            role = Role.objects.get(pk=request.POST.get('role'))
            member = TraditionRole.objects.get(tradition=tradition, role=role, is_approved=True)
            miracle = Miracle.objects.get(pk=request.POST.get('miracle'))
            if miracle.cost <= tradition.mana:
                RoleMiracle.objects.create(owner=role, miracle=miracle)
                tradition.mana -= miracle.cost
                tradition.save()

                send_mail(
                    u"Анклав: вы одарены чудом",
                    u"Иерарх одарил вас чудом '%s'. Вы можете отметить его как примененное на странице http://%s%s ." \
                        % (miracle.name, settings.DOMAIN, reverse('my_miracles')),
                    None,
                    ['linashyti@gmail.com', 'glader.ru@gmail.com', role.profile.user.email]
                )
                return HttpResponseRedirect(reverse('tradition_miracles', args=[tradition.code]))

            else:
                error = u"В традиции недостаточно маны для этого чуда."

        except (Role.DoesNotExist, TraditionRole.DoesNotExist):
            error = u"Неизвестный персонаж"

        except (Miracle.DoesNotExist,):
            error = u"Неизвестное чудо"

    miracles = Miracle.objects.filter(cost__lte=tradition.mana).order_by('cost', 'name')
    members = TraditionRole.objects.filter(tradition=tradition, is_approved=True).exclude(level='master')
    granted_miracles = list(RoleMiracle.objects.filter(owner__in=[member.role_id for member in members]))
    for miracle in granted_miracles:
        miracle.used = miracle.recipient_id is not None

    granted_miracles.sort(key=lambda m: m.used)

    return render_to_response(request, 'tradition_miracles.html',
            {
                'tradition': tradition,
                'members': members,
                'miracles': miracles,
                'granted_miracles': granted_miracles,
                'error': error,
            }
    )


@tradition_required
def tradition_view(request, code):
    tradition = Tradition.objects.get(code=code)
    membership = tradition.membership(request.actual_role)

    if request.POST and request.POST.get('post'):
        TraditionGuestbook.objects.create(
            tradition=tradition,
            author=request.actual_user,
            content=request.POST.get('post'),
        )
        recievers = [tr.role.profile.user.email for tr in TraditionRole.objects.filter(tradition=tradition, is_approved=True, role__profile__isnull=False)] \
                    + ['glader.ru@gmail.com', 'linashyti@gmail.com']
        for email in recievers:
            send_mail(
                u"Анклав: Новая запись",
                u"Новая запись на странице '%s'. http://%s%s" % (tradition.name, settings.DOMAIN, reverse('tradition', args=[tradition.code])),
                None,
                [email],
            )
        return HttpResponseRedirect(reverse('tradition', args=[tradition.code]) + '?save=ok')

    return render_to_response(request, 'tradition.html',
        {
            'tradition': tradition,
            'articles': tradition.traditiontext_set.all(),
            'files': tradition.traditionfile_set.all(),
            'chat': tradition.traditionguestbook_set.all().order_by('-dt_created')[:20],
            'master': membership and membership.level == 'master',
        }
    )


@tradition_required
def edit_tradition(request, code):
    tradition = Tradition.objects.get(code=code)
    membership = tradition.membership(request.actual_role)

    if not (membership and membership.level == 'master'):
        raise Http404

    if request.POST:
        form = TraditionForm(request.POST, instance=tradition)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tradition', args=[tradition.code]) + '?save=ok')
    else:
        form = TraditionForm(instance=tradition)

    return render_to_response(request, 'edit_tradition.html', {'form': form})


@tradition_required
def add_tradition_text(request, code):
    tradition = Tradition.objects.get(code=code)
    if request.POST:
        form = TraditionTextForm(request.POST)
        if form.is_valid():
            TraditionText.objects.create(
                tradition=tradition,
                author=request.actual_user,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
            )
            return HttpResponseRedirect(reverse('tradition', args=[tradition.code]) + '?save=ok')
    else:
        form = TraditionTextForm()

    return render_to_response(request, 'add_tradition_text.html', {'form': form})


@tradition_required
def add_tradition_file(request, code):
    tradition = Tradition.objects.get(code=code)
    if request.POST:
        form = TraditionFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.author = request.user
            file.tradition = tradition
            file.save()
            return HttpResponseRedirect(reverse('tradition', args=[tradition.code]) + '?save=ok')
    else:
        form = TraditionFileForm()

    return render_to_response(request, 'add_tradition_file.html', {'form': form})


@tradition_required
def tradition_text(request, code, number):
    tradition = Tradition.objects.get(code=code)
    text = get_object_or_404(TraditionText, tradition=tradition, pk=number)
    return render_to_response(request, 'tradition_text.html', {'text': text})


@tradition_required
def edit_tradition_text(request, code, number):
    tradition = Tradition.objects.get(code=code)
    text = get_object_or_404(TraditionText, tradition=tradition, pk=number)
    if request.POST:
        form = TraditionTextModelForm(request.POST, instance=text)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tradition_text', args=[tradition.code, text.id]) + '?save=ok')
    else:
        form = TraditionTextModelForm(instance=text)

    return render_to_response(request, 'edit_tradition_text.html', {'form': form})


@login_required
def my_miracles(request):
    miracles = list(RoleMiracle.objects.filter(owner=request.actual_role))
    for miracle in miracles:
        miracle.used = miracle.recipient_id is not None
    miracles.sort(key=lambda m: m.used)

    roles = Role.objects.filter(profile__isnull=False).exclude(pk=request.actual_role.id).order_by('name')

    if request.POST:
        try:
            recipient = Role.objects.get(pk=request.POST.get('role'))
            miracle = RoleMiracle.objects.get(pk=request.POST.get('miracle'), owner=request.actual_role, recipient__isnull=True)
            miracle.recipient = recipient
            miracle.use_dt = datetime.now()
            miracle.save()

            send_mail(
                u"Анклав: чудо применено",
                u"'%s' применил на '%s' чудо '%s'."\
                % (request.actual_role, recipient, miracle.miracle.name),
                None,
                ['linashyti@gmail.com', 'glader.ru@gmail.com', request.actual_role.profile.user.email, recipient.profile.user.email]
            )

            return HttpResponseRedirect(reverse('my_miracles') + '?save=ok')

        except (Role.DoesNotExist, RoleMiracle):
            pass

    return render_to_response(request, 'my_miracles.html', {'miracles': miracles, 'roles': roles})


@role_required
def duels(request):
    log = logging.getLogger('django.duels')

    if request.POST:
        form = CreateDuelForm(request.POST)
        if form.is_valid():
            duel = form.save(request.actual_role)
            log.info("New duel %s", reverse('duel', args=[duel.pk]))
            return HttpResponseRedirect(reverse('duel', args=[duel.pk]))
    else:
        form = CreateDuelForm()

    return render_to_response(request, 'duels.html', {'form': form, 'duels': Duel.objects.filter(Q(role_1=request.actual_role) | Q(role_2=request.actual_role)).order_by('-id')})


@role_required
def target(request):
    context = {
        'person_form': PersonHackTarget(request.actual_role),
        'tradition_form': TraditionHackTarget(request.actual_role),
        }

    if request.POST:
        if request.POST['target'] == 'role':
            context['person_form'] = PersonHackTarget(request.actual_role, request.POST)
            if context['person_form'].is_valid():
                hack = context['person_form'].save()
                return HttpResponseRedirect(reverse('hack_personal', args=[hack.uuid]))

        if request.POST['target'] == 'tradition':
            context['tradition_form'] = TraditionHackTarget(request.actual_role, request.POST)
            if context['tradition_form'].is_valid():
                hack = context['tradition_form'].save()

                # письма машинистам традиции
                security = [role.role.profile.user.email for role in TraditionRole.objects.filter(tradition=hack.get_target(), level='security')]
                send_mail(
                    u"Анклав: атака на вашу Традицию/корпорацию!",
                    u"На вашу структуру '%s' произошло нападение. Встать на защиту можно по ссылке http://%s%s ." % \
                        (hack.get_target().name, settings.DOMAIN, reverse('hack_tradition_security', args=[hack.uuid])),
                    None,
                    security + ['linashyti@gmail.com', 'glader.ru@gmail.com'],
                )
                return HttpResponseRedirect(reverse('hack_tradition', args=[hack.uuid]))

    return render_to_response(request, 'hack_target.html', context)


@role_required
def personal_hack_page(request, uuid):
    hack = get_object_or_404(Hack, uuid=uuid, hacker=request.actual_role)
    context = {
        'hack': hack,
        'moves': hack.hackmove_set.all().order_by('id'),
    }

    if not hack.result and request.POST:
        try:
            number = request.POST.get('number')
            CreateDuelForm.check_number(number, number_len=len(hack.number))

            result = Duel.get_result(hack.number, number)
            context['last_move'] = HackMove.objects.create(
                hack=hack,
                move=number,
                result=result,
            )

            if result == '1' * len(hack.number):
                # отправляем информацию по почте
                send_mail(
                    u"Анклав: успешный взлом",
                    u"Вы взломали данные '%s' жителя '%s'.\n" % (hack.get_field_display(), hack.get_target().name) + hack.get_target_value(),
                    None,
                    [request.user.email, 'linashyti@gmail.com', 'glader.ru@gmail.com']
                )

                # Прекращаем параллельные взломы
                Hack.objects.filter(key=hack.key, result__isnull=True).exclude(pk=hack.pk).update(result='late')

                # Сохраняем результат
                hack.result = 'win'
                hack.save()

                # Акция
                if hack.key.endswith('actions_steal'):
                    actions = list(RoleStock.objects.filter(role=hack.get_target(), amount__gt=0))
                    action = random.choice(actions)
                    action.amount -= 1
                    action.save()

                    new_action, _ = RoleStock.objects.get_or_create(role=request.actual_role, company=action.company)
                    new_action.amount += 1
                    new_action.save()

            if HackMove.objects.filter(hack=hack).count() >= 6:
                hack.result = 'fail'
                hack.save()

            return HttpResponseRedirect(reverse('hack_personal', args=[hack.uuid]))

        except ValidationError, e:
            context['error'] = unicode(e.messages[0])

    return render_to_response(request, 'hack_personal.html', context)


@role_required
def tradition_hack_page_security(request, uuid):
    u"""Выбор защитника"""
    hack = get_object_or_404(TraditionHack, uuid=uuid)

    if not request.actual_role in [role.role for role in TraditionRole.objects.filter(tradition=hack.get_target(), level='security')]:
        raise Http404

    if hack.is_finished or hack.security:
        return HttpResponseRedirect(reverse('hack_tradition', args=[hack.uuid]))

    if request.POST:
        hack.security = request.actual_role
        hack.state = 'in_progress'
        hack.save()

        return HttpResponseRedirect(reverse('hack_tradition', args=[hack.uuid]))

    return render_to_response(request, 'hack_tradition_security.html', {'hack': hack})


@role_required
def tradition_hack_page(request, uuid):
    hack = get_object_or_404(TraditionHack, uuid=uuid)

    if not hack.is_finished and not hack.security:
        # Еще нет защитников
        if request.actual_role in [role.role for role in TraditionRole.objects.filter(tradition=hack.get_target(), level='security')]:
            return HttpResponseRedirect(reverse('hack_tradition_security', args=[hack.uuid]))

    if not (hack.hacker == request.actual_role or hack.security == request.actual_role):
        raise Http404

    context = {
        'hack': hack,
        'moves': list(hack.traditionhackmove_set.all().order_by('id')),
        'mode': request.actual_role == hack.hacker and 'hacker' or 'security',
        'last_move': None,
        'can_move': False,
        }

    if hack.is_finished:
        return render_to_response(request, 'hack_tradition.html', context)

    if len(context['moves']):
        context['last_move'] = context['moves'][-1]

    context['can_move'] = can_move(context['mode'], hack, context['last_move'])

    # Ходы
    if context['can_move'] and request.POST:
        if request.POST.get('action') == 'Сдаться':
            hack.state = 'run'
            hack.winner = hack.security
            hack.save()
            return HttpResponseRedirect(reverse('duels'))

        try:
            number = request.POST.get('number')
            CreateDuelForm.check_number(number)

            if not context['last_move'] or getattr(context['last_move'], '%s_move' % context['mode'], None):
                context['last_move'] = TraditionHackMove.objects.create(
                    hack=hack,
                    dt=datetime.now()
                )
                setattr(context['last_move'], '%s_move' % context['mode'], number)
                context['last_move'].save()

            elif context['mode'] == 'hacker' and not context['last_move'].hacker_move:
                context['last_move'].hacker_move = number
                context['last_move'].save()

            elif context['mode'] == 'security' and not context['last_move'].security_move:
                context['last_move'].security_move = number
                context['last_move'].save()

            if context['last_move'].hacker_result == '1' * len(hack.security_number):
                hack.state = 'win'
                hack.winner = hack.hacker
                hack.save()

                # Отправка на почту взломанной инфы
                send_mail(
                    u"Анклав: успешный взлом",
                    u"Вы взломали данные '%s' компании '%s'.\n" % (hack.get_field_display(), hack.get_target().name) + hack.get_target_value(),
                    None,
                    [request.user.email, 'linashyti@gmail.com', 'glader.ru@gmail.com']
                )

                # Прекращаем параллельные взломы
                TraditionHack.objects.filter(key=hack.key, state='in_progress').exclude(pk=hack.pk).update(result='late')

                return HttpResponseRedirect(reverse('hack_tradition', args=[hack.uuid]))

            if context['last_move'].security_result == '1' * len(hack.hacker_number):
                hack.state = 'lose'
                hack.winner = hack.security
                hack.save()

                # Отправка машинисту на почту имени ломщика
                send_mail(
                    u"Анклав: успешное противостояние взлому",
                    u"Вы защитили данные '%s' компании '%s'.\nЛомщик: %s" % (hack.get_field_display(), hack.get_target().name, hack.hacker.name),
                    None,
                    [request.user.email, 'linashyti@gmail.com', 'glader.ru@gmail.com']
                )
                return HttpResponseRedirect(reverse('hack_tradition', args=[hack.uuid]))

            return HttpResponseRedirect(reverse('hack_tradition', args=[hack.uuid]))

        except ValidationError, e:
            context['error'] = unicode(e.messages[0])

    return render_to_response(request, 'hack_tradition.html', context)


def can_move(mode, hack, last_move):
    now = datetime.now()

    if mode == 'hacker':
        if last_move:
            if last_move.hacker_move and last_move.security_move:  # предыдущий ход сделан обоими сторонами
                return True

            if last_move.security_move:
                return True

            if last_move.hacker_move and (now - last_move.dt).seconds > 20 * 60:
                return True

        else:  # Еще не сделано ни одного хода
            if hack.security or (now - hack.dt).seconds > 20 * 60:
                return True

    elif mode == 'security':
        if last_move:
            if last_move.hacker_move and last_move.security_move:  # предыдущий ход сделан обоими сторонами
                return True

            if last_move.hacker_move:
                return True

            if last_move.security_move and (now - last_move.dt).seconds > 20 * 60:
                return True

        else:  # Еще не сделано ни одного хода
            return True

    return False


@role_required
def duel_page(request, pk):
    log = logging.getLogger('django.duels')

    duel = get_object_or_404(Duel, pk=pk)
    if not (request.actual_role == duel.role_1
            or request.actual_role == duel.role_2
            or request.user.is_superuser):
        raise Http404

    context = {
        'mode': request.actual_role == duel.role_1 and 'hacker' or 'security',
        'moves': list(duel.duelmove_set.all().order_by('dt')),
        'last_move': None,
        'can_move': False,
        'duel': duel,
        'number_len': duel.number_len,
    }

    if duel.state == 'finished':
        return render_to_response(request, 'duel.html', context)

    if len(context['moves']):
        context['last_move'] = context['moves'][-1]

    if duel.state == 'in_progress':
        if context['last_move']:
            if context['last_move'].move_1 and context['last_move'].move_2:  # предыдущий ход сделан обоими сторонами
                context['can_move'] = True

            elif context['mode'] == 'hacker':
                # Ломщик
                if not context['last_move'].move_1:
                    context['can_move'] = True

            else:
                # Машинист
                if not context['last_move'].move_2:
                    context['can_move'] = True

        else:  # Еще не сделано ни одного хода
            context['can_move'] = True

    if context['mode'] == 'security' and duel.state == 'not_started' and request.POST:
        try:
            n = request.POST.get('number')
            CreateDuelForm.check_number(n, number_len=duel.number_len)

            duel.number_2 = n
            duel.state = 'in_progress'
            duel.save()

            log.info("Duel %s: started by security", duel.pk)
            return HttpResponseRedirect(reverse('duel', args=[duel.pk]))

        except ValidationError, e:
            context['error'] = unicode(e.messages[0])

    # Ходы
    if duel.state == 'in_progress' and request.POST:
        if request.POST.get('action') == 'Сдаться':
            duel.state = 'finished'
            duel.winner = duel.role_2
            duel.result = u"Ломщик сбежал"
            duel.save()
            log.info("Duel %s: hacker gave up", duel.pk)
            return HttpResponseRedirect(reverse('duels'))

        try:
            number = request.POST.get('number')
            CreateDuelForm.check_number(number, number_len=duel.number_len)

            log.info("Duel %s: move by %s: %s", duel.pk, context['mode'], number)

            if not context['last_move'] or (context['last_move'].move_1 and context['last_move'].move_2):
                context['last_move'] = DuelMove.objects.create(
                    duel=duel,
                    dt=datetime.now()
                )
                setattr(context['last_move'], 'move_%s' % (context['mode'] == 'hacker' and '1' or '2'), number)
                context['last_move'].save()

            elif context['mode'] == 'hacker' and not context['last_move'].move_1:
                context['last_move'].move_1 = number
                context['last_move'].save()

            elif context['mode'] == 'security' and not context['last_move'].move_2:
                context['last_move'].move_2 = number
                context['last_move'].save()

            if context['last_move'].result_1 == '1' * duel.number_len:
                duel.state = 'finished'
                duel.winner = duel.role_1
                duel.result = u"Ломщик выиграл"
                duel.save()
                log.info("Duel %s: hacker win", duel.pk)
                return HttpResponseRedirect(reverse('duel', args=[duel.pk]))

            if context['last_move'].result_2 == '1' * duel.number_len:
                duel.state = 'finished'
                duel.winner = duel.role_2
                duel.result = u"Машинист выиграл"
                duel.save()
                log.info("Duel %s: security win", duel.pk)
                return HttpResponseRedirect(reverse('duel', args=[duel.pk]))

            return HttpResponseRedirect(reverse('duel', args=[duel.pk]))

        except ValidationError, e:
            context['error'] = unicode(e.messages[0])

    return render_to_response(request, 'duel.html', context)


def dd_required(func):
    def wrapper(request, *args, **kwargs):
        if request.actual_role or request.actual_role.dd_number:
            return func(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('dd'))
    return wrapper


@role_required
def dd(request):
    context = {}

    if request.actual_role.dd_number:
        context['requests'] = DDRequest.objects.all().order_by('-dt')
        context['numbers'] = [role.dd_number for role in Role.objects.filter(dd_number__isnull=False).order_by('dd_number')]
        return render_to_response(request, 'dd_requests.html', context)

    else:
        if request.POST:
            try:
                n = int(request.POST.get('n', ''))

                if Role.objects.filter(dd_number=n).exists() or n in (9, 42):
                    raise ValidationError(u"Этот номер уже занят, выберите другой.")

                request.actual_role.dd_number = n
                request.actual_role.save()
                return HttpResponseRedirect(reverse('dd'))

            except ValueError:
                context['error'] = u"Это не число"
            except ValidationError, e:
                context['error'] = unicode(e.messages[0])

        return render_to_response(request, 'dd_number_form.html', context)


@dd_required
def dd_add(request):
    if request.POST:
        form = DDForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.author = request.actual_user
            req.save()
            return HttpResponseRedirect(reverse('dd_request', args=[req.id]))
    else:
        form = DDForm()

    return render_to_response(request, 'dd_request_add.html', {'form': form})


@dd_required
def dd_request(request, req_id):
    req = get_object_or_404(DDRequest, pk=req_id)

    if request.POST:
        if request.POST.get('action') == u'Написать' and request.POST.get('content'):
            DDComment.objects.create(
                request=req,
                author=request.actual_user,
                content=request.POST.get('content')
            )
            req.send_notification('comment')
            return HttpResponseRedirect(reverse('dd_request', args=[req.id]))

        if req.status == 'created' and request.POST.get('action') == u"Назначить исполнителем" and request.POST.get('n'):
            try:
                role = Role.objects.get(dd_number=request.POST.get('n'))
                user = role.profile.user
                req.assignee = user
                req.status = 'assigned'
                req.save()
                req.send_notification('assigned')
                return HttpResponseRedirect(reverse('dd_request', args=[req.id]))

            except Role.DoesNotExist:
                pass

        if request.POST.get('action') == u'Сделано' and request.user == req.assignee and req.status == 'assigned':
            req.status = 'ready'
            req.save()
            req.send_notification('ready')
            return HttpResponseRedirect(reverse('dd_request', args=[req.id]))

        if request.POST.get('action') == u'Подтверждено' and request.user == req.author and req.status == 'ready':
            req.status = 'done'
            req.save()
            req.send_notification('done')
            return HttpResponseRedirect(reverse('dd_request', args=[req.id]))

        if request.POST.get('action') == u'Провалено' and request.user == req.author:
            req.status = 'fail'
            req.save()
            req.send_notification('fail')
            return HttpResponseRedirect(reverse('dd_request', args=[req.id]))

    return render_to_response(request, 'dd_request.html', {'req': req, 'comments': req.ddcomment_set.all().order_by('dt')})


@dd_required
def dd_messages(request):
    pass


@dd_required
def dd_history(request, recipient_number):
    context = {}

    try:
        recipient = Role.objects.get(dd_number=recipient_number).profile.user
        context['number'] = recipient_number
        context['dd_messages'] = DDMessage.objects.filter(Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user))

        if request.POST and request.POST.get('content'):
            DDMessage.objects.create(
                sender=request.user,
                recipient=recipient,
                content=request.POST.get('content'),
            )
            send_mail(
                u"Анклав: новое сообщение на сервере DD",
                u"Hello, %s. You are waiting at http://%s%s" % (recipient_number, settings.DOMAIN, reverse('dd_history', args=[request.actual_role.dd_number])),
                None,
                [request.user.email, 'linashyti@gmail.com', 'glader.ru@gmail.com']
            )
            return HttpResponseRedirect(reverse('dd_history', args=[recipient_number]))

    except Role.DoesNotExist:
        context['error'] = u"Неизвестный получатель"

    return render_to_response(request, 'dd_history.html', context)


@role_required
def stock(request):
    deals = Deal.objects.filter(is_closed=False).order_by('company')
    actions = RoleStock.objects.filter(role=request.actual_role, amount__gt=0)
    error = u""

    if request.POST:
        try:
            deal = Deal.objects.get(pk=request.POST.get('deal'), is_closed=False)

            if request.actual_role.money >= deal.cost:
                deal.is_closed = True
                deal.dt_closed = datetime.now()
                deal.buyer = request.actual_role
                deal.save()

                if request.actual_role != deal.role:
                    owner = Role.objects.get(pk=deal.role_id)
                    owner.money += deal.cost
                    owner.save()

                    request.actual_role.money -= deal.cost
                    request.actual_role.save()

                action, _ = RoleStock.objects.get_or_create(role=request.actual_role, company=deal.company)
                action.amount += deal.amount
                action.save()

                traders = [role.role.profile.user.email for role in TraditionRole.objects.filter(level='economy')]
                send_mail(
                    u"Анклав: закрыто предложение на бирже",
                    u"Закрыта сделка на %s шт акций компании '%s' по цене %s юаней." % (deal.amount, deal.company.name, deal.cost),
                    None,
                    traders + ['linashyti@gmail.com', 'glader.ru@gmail.com']
                )

                return HttpResponseRedirect(reverse('stock') + '?save=ok')
            else:
                error = u"У вас недостаточно денег для покупки"

        except Deal.DoesNotExist:
            error = u"Сделка не найдена"

    return render_to_response(request, 'stock.html', {'deals': deals, 'actions': actions, 'error': error})


@role_required
def stock_add(request):
    if request.POST:
        form = DealForm(request.actual_role, request.POST)
        if form.is_valid():
            deal = form.save()

            traders = [role.role.profile.user.email for role in TraditionRole.objects.filter(level='economy')]
            send_mail(
                u"Анклав: новое предложение на бирже",
                u"Выложено %s шт акций компании '%s' по цене %s юаней." % (deal.amount, deal.company.name, deal.cost),
                None,
                traders + ['linashyti@gmail.com', 'glader.ru@gmail.com']
            )
            return HttpResponseRedirect(reverse('stock'))

    else:
        form = DealForm(request.actual_role)

    return render_to_response(request, 'stock_add.html', {'form': form})


@role_required
def stock_history(request):
    return render_to_response(request, 'stock_history.html', {'deals': Deal.objects.filter(is_closed=True).order_by('-dt_closed')})


@role_required
def transfer(request):
    if request.POST:
        form = TransferForm(request.actual_role, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('stock') + '?transfer=ok')

    else:
        form = TransferForm(request.actual_role)

    return render_to_response(request, 'transfer.html', {'form': form})
