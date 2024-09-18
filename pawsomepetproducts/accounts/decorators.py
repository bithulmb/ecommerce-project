from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
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

# def superuser_required(
#     view_func=None,
#     redirect_field_name=REDIRECT_FIELD_NAME, 
#     login_url="admin_login"
# ):
#     """
#     Decorator for views that checks that the user is logged in and is a superuser
#     , redirecting to the login page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.is_superadmin,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name,
#     )
#     if view_func:
#         return actual_decorator(view_func)
#     return actual_decorator
