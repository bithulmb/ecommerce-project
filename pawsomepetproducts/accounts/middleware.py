
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse


class BlockUserMiddleware:
    """ Middleware to block user if he has already logged in and then the user is blocked by the admin"""
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        if request.user.is_authenticated:
            if request.user.is_blocked:
                logout(request)
                return redirect(reverse('login_page'))
        response = self.get_response(request)
        return response

