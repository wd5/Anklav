# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template

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

    url('^roles$', direct_to_template, {'template': 'roles.html'}),
    url('^add_role', 'core.views.add_role', name="add_role"),
    url('^form$', 'core.views.form', name="form"),
    url('^$', direct_to_template, {'template': 'index.html'}),

#(r'^', include('core.urls')),
)
