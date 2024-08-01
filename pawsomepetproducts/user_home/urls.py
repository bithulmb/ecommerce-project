from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view, name='home_page'),
    path('about/', views.about_us_view, name='about_us_page'),
    path('contact/', views.contact_us_view, name='contact_us_page'),
    
]