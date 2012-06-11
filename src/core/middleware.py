# -*- coding: utf-8 -*-

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


