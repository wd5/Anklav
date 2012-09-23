# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from .utils import render_to_response
from .models import Tradition, TraditionRole, RoleStock


def role_required(func):
    def wrapper(request, *args, **kwargs):
        if request.actual_role or request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return render_to_response(request, 'role_required.html')
    return wrapper


def tradition_required(func):
    def wrapper(request, *args, **kwargs):
        return func(request, *args, **kwargs)
    return wrapper


def tradition_required_while_game(func):
    def wrapper(request, *args, **kwargs):
        if request.actual_role or request.user.is_superuser:
            try:
                if request.user.is_superuser:
                    return func(request, *args, **kwargs)

                tradition = Tradition.objects.get(code=kwargs['code'])
                if TraditionRole.objects.filter(tradition=tradition, role=request.actual_role, is_approved=True, tradition__type__in=('tradition', 'crime')).exists():
                    return func(request, *args, **kwargs)

                if TraditionRole.objects.filter(tradition=tradition, role=request.actual_role, is_approved=True, tradition__type='corporation').exists() and \
                   RoleStock.objects.filter(role=request.actual_role, company=tradition, amount__gte=1).exists():
                    return func(request, *args, **kwargs)

                if RoleStock.objects.filter(role=request.actual_role, company=tradition, amount__gte=20).exists():
                    return func(request, *args, **kwargs)

            except Tradition.DoesNotExist:
                pass

        raise Http404
    return wrapper


def dd_required(func):
    def wrapper(request, *args, **kwargs):
        if request.actual_role.dd_number:
            return func(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('dd'))
    return wrapper


def online_required(func):
    def wrapper(request, *args, **kwargs):
        if request.actual_role and request.actual_role.online:
            return func(request, *args, **kwargs)
        else:
            return render_to_response(request, 'online_required.html')
    return wrapper