# -*- coding: utf-8 -*-

from django.utils import simplejson
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.db.models import F

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
        if request.actual_role and request.actual_role.tradition:
            return func(request, *args, **kwargs)
        else:
            raise Http404
    return wrapper


@tradition_required
def tradition(request):
    if request.POST and request.POST.get('post'):
        TraditionGuestbook.objects.create(
            tradition=request.actual_role.tradition,
            author=request.actual_user,
            content=request.POST.get('post'),
        )
        return HttpResponseRedirect(reverse('tradition') + '?save=ok')

    return render_to_response(request, 'tradition.html',
        {
            'tradition': request.actual_role.tradition,
            'articles': request.actual_role.tradition.traditiontext_set.all(),
            'chat': request.actual_role.tradition.traditionguestbook_set.all().order_by('-dt_created')[:20]
        }
    )


@tradition_required
def edit_tradition(request):
    if request.POST:
        form = TraditionForm(request.POST, instance=request.actual_role.tradition)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tradition') + '?save=ok')
    else:
        form = TraditionForm(instance=request.actual_role.tradition)

    return render_to_response(request, 'edit_tradition.html', {'form': form})


@tradition_required
def add_tradition_text(request):
    if request.POST:
        form = TraditionForm(request.POST, instance=request.actual_role.tradition)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tradition') + '?save=ok')
    else:
        form = TraditionForm(instance=request.actual_role.tradition)

    return render_to_response(request, 'edit_tradition.html', {'form': form})

