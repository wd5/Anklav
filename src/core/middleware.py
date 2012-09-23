# -*- coding: utf-8 -*-
import logging
from django.contrib.auth.models import User

from .models import Profile, TraditionRole, RoleStock, Tradition

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

            change_user = request.GET.get('change_user') or request.POST.get('change_user')
            if change_user and request.user.is_superuser:
                try:
                    request.actual_user = User.objects.get(pk=change_user)
                    request.actual_profile = request.actual_user.get_profile()
                    if request.actual_profile.role and request.actual_profile.role.profile == request.actual_profile:
                        request.actual_role = request.actual_profile.role

                except User.DoesNotExist:
                    pass

        if request.actual_role:
            request.actual_role.companies = Tradition.objects.all().order_by('name')
            return

            if request.user.is_superuser:
                request.actual_role.companies = Tradition.objects.all().order_by('name')

            else:
                request.actual_role.companies = set()
                for traditionrole in TraditionRole.objects.filter(role=request.actual_role, is_approved=True):
                    if traditionrole.tradition.type in ('tradition', 'crime'):
                        request.actual_role.companies.add(traditionrole.tradition)

                    elif RoleStock.objects.filter(role=request.actual_role, company=traditionrole.tradition, amount__gte=1):
                        request.actual_role.companies.add(traditionrole.tradition)

                for actions in RoleStock.objects.filter(role=request.actual_role, amount__gte=20):
                    request.actual_role.companies.add(actions.company)


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