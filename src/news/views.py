# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.forms.models import modelform_factory
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import CommonNews

from src.core.utils import email, make_pages
from src.core.models import TraditionRole


def render_to_response(request, template_name, context_dict=None):
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict or {})
    return _render_to_response(template_name, context_instance=context)


CommonNewsModelForm = modelform_factory(CommonNews, fields=('title', 'content',))


def common_news(request):
    context = make_pages(CommonNews.objects.all().order_by('-dt'),
        10,
        request.GET.get('page')
    )
    context['url'] = reverse('common_news')
    return render_to_response(request, 'news/commonnews_list.html', context)


@login_required
def add_common_news(request):
    if request.POST:
        form = CommonNewsModelForm(request.POST)
        if form.is_valid():
            obj = CommonNews.objects.create(
                author=request.actual_user,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
            )

            email(
                u"Анклав: новая заметка в газете",
                u"В газету добавлена новая заметка. Читать: http://%s%s \n\n%s" % (settings.DOMAIN, reverse('common_news'), form.cleaned_data['content']),
                [role.role.profile.user.email for role in TraditionRole.objects.filter(level='media')]
            )
            return HttpResponseRedirect(reverse('common_news_item', args=[obj.pk]))
    else:
        form = CommonNewsModelForm()

    return render_to_response(request, 'news/commonnews_add.html', {'form': form})


@login_required
def edit_common_news(request, pk):
    post = get_object_or_404(CommonNews, pk=pk)
    if not request.user == post.author:
        raise Http404

    if request.POST:
        form = CommonNewsModelForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('common_news_item', args=[post.pk]))
    else:
        form = CommonNewsModelForm(instance=post)

    return render_to_response(request, 'news/commonnews_add.html', {'form': form})