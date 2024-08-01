from django.urls import path, include
from . import views




urlpatterns = [

    path('', views.admin_users_view, name='admin_users'),
    path('login/', views.login_view, name='login_page'),
    path('signup/', views.signup_view, name='signup_page'),
    path('logout/', views.logout_view, name='logout_page'),
  
    
]