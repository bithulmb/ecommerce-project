from django.shortcuts import render
from accounts.models import CustomUser


# Create your views here.


#view fucnction for login page of admin
def admin_login_view(request):
    return render(request, 'admin/admin_login.html')


#view function of dashboard page after logging in
def admin_dashboard_view(request):
    return render(request, 'admin/admin_dashboard.html')






