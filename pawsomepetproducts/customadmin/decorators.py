from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def superuser_required(view_func):
    """Decorator for checking whether the request is from a superuser"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('admin_login')
        
        if not request.user.is_superadmin:                
            return HttpResponseForbidden(
                "You do not have permission to access this page."
            )           
            
        return view_func(request, *args, **kwargs)

    return _wrapped_view
