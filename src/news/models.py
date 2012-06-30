# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup, Comment as HtmlComment

from django.contrib.auth.models import User
from django.db import models


class News(models.Model):
    content = models.TextField(verbose_name=u"Содержание")
    dt = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания")

    def __unicode__(self): return self.content

    class Meta:
        verbose_name = u"Админская новость"
        verbose_name_plural = u"Админские новости"
        ordering = ('-dt',)


def sanitizeHTML(value, mode='none'):
    """ Удаляет из value html-теги.
        Если mode==none - все теги
        Если mode==strict - все теги кроме разрешенных
    """
    if mode == 'strict':
        valid_tags = 'p i strong b u a h1 h2 h3 pre br div span img blockquote glader youtube cut blue object param embed iframe'.split()
    else:
        valid_tags = []
    valid_attrs = 'href src pic user page class text title alt'.split()
    # параметры видеороликов
    valid_attrs += 'width height classid codebase id name value flashvars allowfullscreen allowscriptaccess quality src type bgcolor base seamlesstabbing swLiveConnect pluginspage data frameborder'.split()

    soup = BeautifulSoup(value)
    for comment in soup.findAll(
        text=lambda text: isinstance(text, HtmlComment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        tag.attrs = [(attr, val) for attr, val in tag.attrs
                                 if attr in valid_attrs]
    result = soup.renderContents().decode('utf8')
    return result


class CommonNews(models.Model):
    author = models.ForeignKey(User, verbose_name=u"Автор")
    title = models.CharField(verbose_name=u"Заголовок", max_length=100)
    content = models.TextField(verbose_name=u"Содержание")
    dt = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания")

    def __unicode__(self): return self.title

    def save(self, *args, **kwargs):
        self.content = sanitizeHTML(self.content)
        super(CommonNews, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Новость"
        verbose_name_plural = u"Новости"
        ordering = ('-dt',)