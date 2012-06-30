# -*- coding: utf-8 -*-

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
        if request.actual_role:
            try:
                tradition = Tradition.objects.get(code=kwargs['code'])
                if request.actual_role.tradition == tradition or \
                    request.actual_role.corporation == tradition or\
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