# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
    url(r'^/member/(\d+).html$', 'contest.views.member_view', name='contest_member'),
    url(r'^/member/(\d+)/edit$', 'contest.views.member_edit', name='contest_edit'),
    url('^/add$', 'contest.views.add', name='contest_add'),
    url('^$', 'contest.views.index', name='contest_index'),
)
