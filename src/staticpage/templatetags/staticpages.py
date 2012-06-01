# encoding: utf-8

from django import template
from ..models import Article

register = template.Library()


@register.simple_tag()
def content(article_id):
    return Article.objects.get(pk=article_id).content