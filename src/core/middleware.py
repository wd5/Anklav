# -*- coding: utf-8 -*-
import logging

from .models import Profile, Role

class Prepare:
    def process_request(self, request):
        request.profile = None
        request.role = None
        if request.user.is_authenticated():
            try:
                profile = request.user.get_profile()
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=request.user)
            request.profile = profile

            if profile.role and profile.role.profile == profile:
                request.role = profile.role


class LogPost:
    def process_request(self, request):
        if request.POST:
            log = logging.getLogger('django.post')
            report = u"POST\n"
            if request.user.is_authenticated():
                report += u"Игрок: %s\n" % request.user.username
            if request.profile:
                report += u"Профиль: %s\n" % request.profile
                if request.profile.role:
                    report += u"Роль: %s\n" % request.profile.role
            if request.role:
                report += u"Замороженная роль: %s\n" % request.role

            report += request.META['PATH_INFO'] + "\n"
            for k, v in request.POST.items():
                report += u"%s: %s\n" % (k, v)

            log.info(report)