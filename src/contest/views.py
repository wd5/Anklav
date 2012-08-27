# -*- coding: utf-8 -*-

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404

#from .forms import *
from .models import ContestMember, ContestVote


def render_to_response(request, template_name, context_dict=None):
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict or {})
    return _render_to_response(template_name, context_instance=context)


def index(request):
    members = ContestMember.objects.all()

    return render_to_response(request, 'contest/index.html', {'members': members})



def member(request):
    members = ContestMember.objects.all()

    return render_to_response(request, 'contest/index.html', {'members': members})