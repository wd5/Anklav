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


@login_required
def form(request):
    if request.POST:
        if request.profile.role:
            form = RoleForm(request.POST, instance=request.profile.role)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('form') + '?save=ok')
            return render_to_response(request, 'form.html', {'form': form})

    else:
        if request.profile.role:
            form = RoleForm(instance=request.profile.role)
            return render_to_response(request, 'form.html', {'form': form})

    free_roles = Role.objects.filter(profile__isnull=True)
    if free_roles:
        return render_to_response(request, 'choose_role.html', {'free_roles': free_roles})
    else:
        return add_role(request)


@login_required
def add_role(request):
    if request.role:
        # За пользователем уже закреплена роль
        return HttpResponseRedirect("/")

    if request.POST:
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            request.profile.role = role
            request.profile.save()
            return HttpResponseRedirect(reverse('form'))

    else:
        form = RoleForm()

    return render_to_response(request, 'add_role.html', {'form': form})