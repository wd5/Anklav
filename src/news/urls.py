# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import News, CommonNews

urlpatterns = patterns('',
    url(r'^/site.html$', ListView.as_view(queryset=News.objects.all()), name='site_news'),
    url(r'^/common.html$', 'news.views.common_news', name='common_news'),
    url(r'^/common/(?P<pk>\d+).html$', DetailView.as_view(model=CommonNews), name='common_news_item'),
    url(r'^/common/(?P<pk>\d+)/edit$', 'news.views.edit_common_news', name='common_news_item_edit'),
    url(r'^/common/add.html$', 'news.views.add_common_news', name='common_news_add'),
)
