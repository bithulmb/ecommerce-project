from django.urls import path
from . import views


urlpatterns = [
    path('',views.admin_login_view, name='admin_login'),
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('users/', views.admin_users_view, name='admin_users'),
    # path('products/', views.all_products_view, name='all_products_page'),
    # path('about/', views.about_us_view, name='about_us_page'),
    # path('contact/', views.contact_us_view, name='contact_us_page'),
]