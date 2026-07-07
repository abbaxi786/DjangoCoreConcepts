import functools
from django.contrib.auth.models import Group


def CheckUserGroup(group_name):
    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name__in=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden("You do not have permission to access this resource.")
        return _wrapped_view
    return decorator

