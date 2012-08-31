# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail, TemplateView

from core.models import Role
from news.feeds import NewsFeed

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^auth/registration$', 'core.views.registration', name='registration'),
    url(r'^auth/login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^auth/logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^auth/password_reset$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^auth/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^auth/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^auth/reset/done/$', 'django.contrib.auth.views.password_reset_complete'),

    url(r'^admin/', include(admin.site.urls), name="admin"),
    (r'^articles', include('staticpage.urls')),
    (r'^news', include('news.urls')),

    url('^roles$',  'core.views.roles', name='roles'),
    url('^add_role', 'core.views.add_role', name="add_role"),
    url('^choose_role', 'core.views.choose_role', name="choose_role"),
    url('^form$', 'core.views.form', name="form"),
    url('^profile', 'core.views.profile', name="profile"),
    url('^change_user/(\d+)$', 'core.views.change_user', name="change_user"),
    url('^lock_role/(\d+)$', 'core.views.lock_role', name="lock_role"),

    url('^hack$', TemplateView.as_view(template_name="hack.html"), name="hack"),
    url('^hack/duels$', 'core.views.duels', name="duels"),
    url('^hack/duels/(\d+)$', 'core.views.duel_page', name="duel"),

    url('^groups$', 'core.views.traditions_request', name='traditions_request'),
    url('^groups/(?P<code>\w+)$', 'core.views.tradition_view', name="tradition"),
    url('^groups/(?P<code>\w+)/edit$', 'core.views.edit_tradition', name="edit_tradition"),
    url('^groups/(?P<code>\w+)/add$', 'core.views.add_tradition_text', name="add_tradition_text"),
    url('^groups/(?P<code>\w+)/add_file$', 'core.views.add_tradition_file', name="add_tradition_file"),
    url('^groups/(?P<code>\w+)/(?P<number>\d+)$', 'core.views.tradition_text', name="tradition_text"),
    url('^groups/(?P<code>\w+)/(?P<number>\d+)/edit$', 'core.views.edit_tradition_text', name="edit_tradition_text"),
    url('^groups/(?P<code>\w+)/request$', 'core.views.tradition_request', name="tradition_request"),
    url('^groups/(?P<code>\w+)/members', 'core.views.tradition_members', name="tradition_members"),

    url('^dd$', 'core.views.dd', name="dd"),
    url('^dd/add$', 'core.views.dd_add', name="dd_add"),
    url('^dd/(\d+)$', 'core.views.dd_request', name="dd_request"),

    (r'^messages', include('role_message.urls')),
    (r'^contest', include('contest.urls')),

    (r'^feeds/news', NewsFeed()),

    url('^$', direct_to_template, {'template': 'index.html'}),

#(r'^', include('core.urls')),
)
