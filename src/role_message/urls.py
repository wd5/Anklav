# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include, handler404, handler500

urlpatterns = patterns('',
    url(r'^/compose/$', 'role_message.views.messages_compose', name='messages_compose'),
    url(r'^/reply/(\d+)/$', 'role_message.views.reply', name='messages_compose'),
    (r'^/', include('messages.urls')),
)