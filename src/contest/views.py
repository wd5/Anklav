# -*- coding: utf-8 -*-

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from .models import ContestMember, ContestVote, ContestMemberForm


def render_to_response(request, template_name, context_dict=None):
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict or {})
    return _render_to_response(template_name, context_instance=context)


def index(request):
    members = ContestMember.objects.all()
    can_add = request.user.is_authenticated() and not ContestMember.objects.filter(user=request.user).exists()

    return render_to_response(request, 'contest/index.html', {'members': members, 'can_add': can_add})


def add(request):
    if ContestMember.objects.filter(user=request.user).exists():
        raise Http404

    if request.POST:
        form = ContestMemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            return HttpResponseRedirect(reverse('contest_member', args=[member.id]))
    else:
        form = ContestMemberForm()

    return render_to_response(request, 'contest/add.html', {'form': form})


def member_edit(request, member_id):
    member = get_object_or_404(ContestMember, pk=member_id)
    if member.user != request.user:
        raise Http404

    if request.POST:
        form = ContestMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            return HttpResponseRedirect(reverse('contest_member', args=[member.id]))
    else:
        form = ContestMemberForm(instance=member)

    return render_to_response(request, 'contest/edit.html', {'form': form, 'member': member})


def member_view(request, member_id):
    member = get_object_or_404(ContestMember, pk=member_id)
    context = {
        'member': member,
        'can_edit': member.user == request.user,
        'can_vote': request.user.is_authenticated() and not ContestVote.objects.filter(author=request.user).exists(),
        'voted': request.user.is_authenticated() and ContestVote.objects.filter(author=request.user, member=member).exists(),
    }

    if request.GET.get('action') == 'vote' and context['can_vote']:
        ContestVote.objects.create(author=request.user, member=member)
        member.count += 1
        member.save()
        return HttpResponseRedirect(reverse('contest_member', args=[member.id]))

    if request.GET.get('action') == 'cancel' and context['voted']:
        ContestVote.objects.filter(author=request.user, member=member).delete()
        member.count -= 1
        member.save()
        return HttpResponseRedirect(reverse('contest_member', args=[member.id]))

    return render_to_response(request, 'contest/member.html', context)