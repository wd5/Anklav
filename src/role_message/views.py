# -*- coding: utf-8 -*-
from django.utils import simplejson

from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from messages.models import Message
from django.core.urlresolvers import reverse
from django.db.models import Q

from .forms import ComposeForm
from src.core.models import Role


def render_to_response(request, template_name, context_dict=None):
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict or {})
    return _render_to_response(template_name, context_instance=context)


@login_required
def history(request):
    messages = Message.objects.filter(Q(sender=request.user)|Q(recipient=request.user))
    history = u"\n\n==========================================\n\n".join(
        u"От кого: %s\nКому: %s\nКогда: %s\n%s" % \
        (
            message.sender.get_profile().role.name,
            message.recipient.get_profile().role.name,
            message.sent_at,
            message.body,
        ) for message in messages
    ) or u"Сообщений нет."

    return render_to_response(request, 'messages/history.html', {'history': history.replace('\n', '<br>'),})


def __messages_compose(request):
    from messages.views import compose
    recipient = None
    if request.method == 'GET' and request.GET.get('recipient'):
        role = Role.objects.get(pk=request.GET.get('recipient'))
        recipient = str(role.id)
    return compose(request, recipient=recipient, form_class=ComposeForm)


@login_required
def messages_compose(request, template_name='messages/compose.html', success_url=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfull submission
    """
    if request.method == "POST":
        sender = request.user
        form = ComposeForm(request.POST)
        if form.is_valid():
            form.save(sender=request.user)
            request.user.message_set.create(
                message=_(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            if request.GET.has_key('next'):
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
    else:
        form = ComposeForm(initial=request.GET)

    return render_to_response(request, template_name, {
        'form': form,
        })


@login_required
def reply(request, message_id, form_class=ComposeForm,
          template_name='messages/compose.html', success_url=None, recipient_filter=None):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote.
    """
    from messages.utils import format_quote
    parent = get_object_or_404(Message, id=message_id)

    if parent.sender != request.user and parent.recipient != request.user:
        raise Http404

    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST)
        if form.is_valid():
            form.save(sender=request.user, parent_msg=parent)
            request.user.message_set.create(
                message=_(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            return HttpResponseRedirect(success_url)
    else:
        form = form_class({
            'body': _(u"%(sender)s wrote:\n%(body)s") % {
                'sender': parent.sender.get_profile().role.name,
                'body': format_quote(parent.body)
            },
            'subject': _(u"Re: %(subject)s") % {'subject': parent.subject},
            'recipient': parent.sender.get_profile().role_id
        })
    return render_to_response(request, template_name, {
        'form': form,
        })

