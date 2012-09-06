# encoding: utf-8

from django import template
from ..models import News

register = template.Library()


@register.inclusion_tag("last_news.html")
def last_news():
    return {'news': News.objects.all()[:5]}


@register.filter
def add_page(url, page):
    if page > 1:
        if '?' in url:
            url += '&'
        else:
            url += '?'
        return url + 'page=%s' % page
    else:
        return url