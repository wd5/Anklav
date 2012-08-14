# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import News, CommonNews

urlpatterns = patterns('',
    url(r'^/site$', ListView.as_view(queryset=News.objects.all()), name='site_news'),
    url(r'^/common$', ListView.as_view(queryset=CommonNews.objects.all()), name='common_news'),
    url(r'^/common/(?P<pk>\d+)$', DetailView.as_view(model=CommonNews), name='common_news_item'),
    url(r'^/common/(?P<pk>\d+)/edit$', 'news.views.edit_common_news', name='common_news_item_edit'),
    url(r'^/common/add$', 'news.views.add_common_news', name='common_news_add'),
)
