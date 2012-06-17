# -*- coding: utf-8 -*-
import logging
from django.contrib.auth.models import User

from .models import Profile, Role

class Prepare:
    def process_request(self, request):
        request.profile = None
        request.role = None

        request.actual_user = request.user
        request.actual_profile = None
        request.actual_role = None

        if request.user.is_authenticated():
            try:
                profile = request.user.get_profile()
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=request.user)
            request.actual_profile = request.profile = profile

            if profile.role and profile.role.profile == profile:
                request.actual_role = request.role = profile.role

            if 'change_user' in request.GET and request.user.is_superuser:
                try:
                    request.actual_user = User.objects.get(pk=request.GET['change_user'])
                    request.actual_profile = request.actual_user.get_profile()
                    if request.actual_profile.role and request.actual_profile.role.profile == request.actual_profile:
                        request.actual_role = request.actual_profile.role

                except User.DoesNotExist:
                    pass


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
            for key in sorted(request.POST.keys()):
                report += u"%s: %s\n" % (key, request.POST[key])

            log.info(report)