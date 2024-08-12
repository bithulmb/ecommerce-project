from django.urls import path
from . import views
from accounts import views as account_views
from product import views as product_views
from cart import views as cart_views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('',views.home_view, name='home_page'),
    path('about/', views.about_us_view, name='about_us_page'),
    path('contact/', views.contact_us_view, name='contact_us_page'),

    #views from account app
            
    path('login/', account_views.login_view, name='login_page'),
    path('logout/', account_views.logout_view, name='logout_page'),

        #reset password views from django all auth views
    path('login/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('login/password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('login/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

            #registration section
    path('signup/', account_views.signup_view, name='signup_page'),
    path('verify-otp/', account_views.verify_otp_view, name='verify_otp'),
    path('resend-otp/', account_views.resend_otp_view, name='resend_otp'),
    



            #user profile section
    path('user/profile/', account_views.user_profile_view, name='user_profile'),
    path('user/change-password/',account_views.user_change_password_view, name='change_password'),
    path('user/addresses/',account_views.user_addresses_view,name='user_addresses'),
    path('user/add-address/',account_views.user_add_address_view,name='add_address'),
    path('user/set_default_address/', account_views.user_set_default_address_view, name='set_default_address'),
    path('user/edit-address/<int:pk>', account_views.user_edit_address_view, name='edit_address'),
    path('user/delete-address/<int:pk>', account_views.user_delete_address_view, name='delete_address'),
    
    
    #views from product app
    path('products/', product_views.all_products_view, name='all_products_page'),  #userside all products page
    path('products/<int:pk>',product_views.single_product_view, name='single_product_page'),

    #views from cart app
    path('cart/', cart_views.cart_view, name='cart_page'),
    path('cart/add/<int:variant_id>', cart_views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<int:variant_id>', cart_views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/delete/<int:variant_id>', cart_views.delete_cart_item_view, name='delete_cart_item'),

    
]