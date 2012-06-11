# encoding: utf-8

from django import template
from ..models import News

register = template.Library()


@register.inclusion_tag("last_news.html")
def last_news():
    return {'news': News.objects.all()[:5]}