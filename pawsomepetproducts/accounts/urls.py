from django.urls import path, include
from . import views




urlpatterns = [

    path('', views.admin_users_view, name='admin_users'),
  
    
]