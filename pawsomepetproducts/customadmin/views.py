from django.shortcuts import render,redirect
from accounts.models import CustomUser
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from .decorators import superuser_required
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import requests


# Create your views here.

#view function for redirecting to login page
def admin_panel_view(request):
    return redirect('admin_login')


#view funntion for admin login page
@never_cache
def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        return redirect('admin_dashboard')
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_superadmin:
                login(request,user)

                #for redirecting to the url mentioned in next while logging in
                url=request.META.get('HTTP_REFERER')
                try:
                    query=requests.utils.urlparse(url).query
                    params=dict(x.split("=") for x in query.split("&"))
                    if 'next' in params:
                        nextPage=params['next']
                        return redirect(nextPage)
                except:
                    pass
                return redirect('admin_dashboard')
            else:
                messages.error(request,'You are not authorised to access the details')
        else:
            messages.error(request,"Invalid credentials") 
            
    return render(request,'admin/admin_login.html')




#view function of dashboard page after logging in
@never_cache
@staff_member_required(login_url="admin_login")
def admin_dashboard_view(request):
    return render(request, 'admin/admin_dashboard.html')



#view function for logging out admin
@never_cache
def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')


