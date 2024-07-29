from django.shortcuts import render
from accounts.models import CustomUser

# Create your views here.

def admin_login_view(request):
    return render(request, 'admin/admin_login.html')

def admin_dashboard_view(request):
    return render(request, 'admin/admin_dashboard.html')

def admin_users_view(request):
    users=CustomUser.objects.all()
    return render(request, 'admin/admin_users.html', {'users':users})