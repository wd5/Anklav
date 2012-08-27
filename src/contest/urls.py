# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
    url(r'^member/(\d+)$', 'contest.views.member', name='contest_member'),
    url('^$', 'contest.views.index', name='contest_index'),
)
