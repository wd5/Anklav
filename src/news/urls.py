# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic import list_detail

from .models import News

urlpatterns = patterns('',
    url(r'^$', list_detail.object_list, {"queryset": News.objects.all()}, name='news'),
)
