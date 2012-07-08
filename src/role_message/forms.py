# -*- coding: utf-8 -*-

from django.forms import *
from django.conf import settings
import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from core.models import Role


from messages.models import Message

class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """
    recipient = forms.CharField(label=_(u"Recipient"), widget=Select)
    subject = forms.CharField(label=_(u"Subject"))
    body = forms.CharField(label=_(u"Body"),
        widget=forms.Textarea(attrs={'rows': '12', 'cols':'55'}))


    def __init__(self, *args, **kwargs):
        super(ComposeForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].widget.choices = [(role.pk, role.name)\
        for role in Role.objects.filter(profile__isnull=False).order_by('name')]


    def save(self, sender, parent_msg=None):
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        message_list = []
        role = Role.objects.get(pk=self.cleaned_data['recipient'])
        user = role.profile.user
        msg = Message(
            sender = sender,
            recipient = user,
            subject = subject,
            body = body,
        )
        if parent_msg is not None:
            msg.parent_msg = parent_msg
            parent_msg.replied_at = datetime.datetime.now()
            parent_msg.save()
        msg.save()
        message_list.append(msg)

        send_mail(
            u"Анклав: новое сообщение в личных",
            u"Вам было послано сообщение. Вы можете прочитать его по ссылке http://%s%s" % (settings.DOMAIN, reverse('messages_inbox')),
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        return message_list
