from django.shortcuts import render
from .models import CustomUser

# Create your views here.


def admin_users_view(request):
    users=CustomUser.objects.all()
    return render(request, 'admin/admin_users.html', {'users':users})
