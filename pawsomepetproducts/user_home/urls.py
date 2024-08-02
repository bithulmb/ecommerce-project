from django.urls import path
from . import views
from accounts import views as account_views
from product import views as product_views


urlpatterns = [
    path('',views.home_view, name='home_page'),
    path('about/', views.about_us_view, name='about_us_page'),
    path('contact/', views.contact_us_view, name='contact_us_page'),
    #views from account app
    path('login/', account_views.login_view, name='login_page'),
    path('signup/', account_views.signup_view, name='signup_page'),
    path('logout/', account_views.logout_view, name='logout_page'),
    #views from product app
    path('products/', product_views.all_products_view, name='all_products_page'),  #userside all products page
    path('products/<int:pk>',product_views.single_product_view, name='single_product_page'),
    
]