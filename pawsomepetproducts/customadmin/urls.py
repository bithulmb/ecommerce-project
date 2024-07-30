from django.urls import path, include
from . import views



#url patterns in the admin panel
urlpatterns = [
    path('',views.admin_login_view, name='admin_login'),
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('users/', include('accounts.urls')),
    path('category/', include('category.urls')),
    path('pet-type/', include('pet_type.urls')),

    
]