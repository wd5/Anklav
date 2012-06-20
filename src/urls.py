# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail

from core.models import Role

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

    url('^roles$', list_detail.object_list, {"queryset": Role.objects.all().order_by('location', 'name')}, name='roles'),
    url('^add_role', 'core.views.add_role', name="add_role"),
    url('^choose_role', 'core.views.choose_role', name="choose_role"),
    url('^form$', 'core.views.form', name="form"),
    url('^profile', 'core.views.profile', name="profile"),
    url('^change_user/(\d+)$', 'core.views.change_user', name="change_user"),

    url('^tradition$', 'core.views.tradition', name="tradition"),
    url('^tradition/edit$', 'core.views.edit_tradition', name="edit_tradition"),
    url('^tradition/add$', 'core.views.add_tradition_text', name="add_tradition_text"),

    url('^$', direct_to_template, {'template': 'index.html'}),

#(r'^', include('core.urls')),
)
