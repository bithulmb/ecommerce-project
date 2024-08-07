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
    path('logout/', account_views.logout_view, name='logout_page'),
            #registration section
    path('signup/', account_views.signup_view, name='signup_page'),
    path('verify-otp/', account_views.verify_otp_view, name='verify_otp'),


            #user profile section
    path('user/profile/', account_views.user_profile_view, name='user_profile'),
    path ('user/change-password/',account_views.user_change_password_view, name='change_password'),
    path('user/addresses/',account_views.user_addresses_view,name='user_addresses'),
    path('user/add-address/',account_views.user_add_address_view,name='add_address'),
    path('user/set_default_address/', account_views.user_set_default_address_view, name='set_default_address'),
    path('user/edit-address/<int:pk>', account_views.user_edit_address_view, name='edit_address'),
    path('user/delete-address/<int:pk>', account_views.user_delete_address_view, name='delete_address'),
    
    
    #views from product app
    path('products/', product_views.all_products_view, name='all_products_page'),  #userside all products page
    path('products/<int:pk>',product_views.single_product_view, name='single_product_page'),
    
]