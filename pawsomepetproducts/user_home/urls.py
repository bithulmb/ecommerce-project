from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_page_view, name='home_page'),
    path('login/', views.login_page_view, name='login_page'),
    path('signup/',views.signup_page_view, name='signup_page'),
]