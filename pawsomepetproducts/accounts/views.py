from django.shortcuts import render
from .models import CustomUser
from django.db.models import Q

# Create your views here.

#view function for listing the users in admin panel
def admin_users_view(request):
    query=request.GET.get('q')
    if query:   #if there is search query
        users=CustomUser.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query))
    else:
        users=CustomUser.objects.all()
    return render(request, 'admin/admin_users.html', {'users':users})
