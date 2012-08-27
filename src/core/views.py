# -*- coding: utf-8 -*-
from datetime import datetime
import logging

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


def tradition_required(func):
    def wrapper(request, *args, **kwargs):
        if request.actual_role or request.user.is_superuser:
            try:
                tradition = Tradition.objects.get(code=kwargs['code'])
                if request.user.is_superuser or \
                    request.actual_role.tradition == tradition or \
                    request.actual_role.corporation == tradition or \
                    request.actual_role.crime == tradition:
                        return func(request, *args, **kwargs)

            except Tradition.DoesNotExist:
                pass

        raise Http404
    return wrapper


@tradition_required
def tradition(request, code):
    tradition = Tradition.objects.get(code=code)
    if request.POST and request.POST.get('post'):
        TraditionGuestbook.objects.create(
            tradition=tradition,
            author=request.actual_user,
            content=request.POST.get('post'),
        )
        return HttpResponseRedirect(reverse('tradition', args=[tradition.code]) + '?save=ok')

    return render_to_response(request, 'tradition.html',
        {
            'tradition': tradition,
            'articles': tradition.traditiontext_set.all(),
            'chat': tradition.traditionguestbook_set.all().order_by('-dt_created')[:20]
        }
    )


@tradition_required
def edit_tradition(request, code):
    tradition = Tradition.objects.get(code=code)
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
def duels(request):
    log = logging.getLogger('django.duels')

    if request.actual_role and request.POST:
        form = CreateDuelForm(request.POST)
        if form.is_valid():
            duel = form.save(request.actual_role)
            log.info("New duel %s", reverse('duel', args=[duel.pk]))
            return HttpResponseRedirect(reverse('duel', args=[duel.pk]))
    else:
        form = CreateDuelForm()

    return render_to_response(request, 'duels.html', {'form': form, 'duels': Duel.objects.all().order_by('-id')})


@login_required
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
            if context['last_move'].move_1 and context['last_move'].move_2: # предыдущий ход сделан обоими сторонами
                context['can_move'] = True

            elif context['mode'] == 'hacker':
                # Ломщик
                if not context['last_move'].move_1:
                    context['can_move'] = True

            else:
                # Машинист
                if not context['last_move'].move_2:
                    context['can_move'] = True

        else: # Еще не сделано ни одного хода
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


@login_required
def dd(request):
    context = {}
    if request.actual_role.dd_number:
        context['requests'] = DDRequest.objects.filter(status='created').order_by('-dt')
        return render_to_response(request, 'dd_requests.html', context)

    else:
        if request.POST:
            try:
                n = int(request.POST.get('n', ''))

                if Role.objects.filter(dd_number=n).exists() or n in (9, 42):
                    raise ValidationError(u"Этот номеро уже занят, выберите другой.")

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
    if req.status != 'created':
        if not (request.user in (req.author, req.assignee) or request.user.is_superuser):
            raise Http404

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