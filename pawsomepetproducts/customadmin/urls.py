from django.urls import path, include
from . import views
from pet_type.views import admin_pet_type_view



urlpatterns = [
    path('',views.admin_login_view, name='admin_login'),
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('users/', include('accounts.urls')),
    path('category/', include('category.urls')),
    path('pet-type/', include('pet_type.urls')),
    # path('contact/', views.contact_us_view, name='contact_us_page'),
    
]