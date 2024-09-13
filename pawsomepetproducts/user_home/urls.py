from django.urls import path
from . import views
from accounts import views as account_views
from product import views as product_views
from cart import views as cart_views
from orders import views as order_views 
from django.contrib.auth import views as auth_views
from wishlist import views as wishlist_views
from coupons import views as coupon_views
from wallet import views as wallet_views


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

        #mobile number verifiation
    path('user/request-mobile-otp/', account_views.request_mobile_otp_view, name='request_mobile_otp'),
    path('user/verify-mobile-otp/', account_views.verify_mobile_otp_view, name='verify_mobile_otp'),
    



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
    path('products/search/',product_views.search_products_view, name='search_products'),
    path('products/<int:variant_id>/submit-review',product_views.submit_review_view, name='submit_review'),



    #views from cart app
    path('cart/', cart_views.cart_view, name='cart_page'),
    path('cart/add/<int:variant_id>', cart_views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<int:variant_id>', cart_views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/delete/<int:variant_id>', cart_views.delete_cart_item_view, name='delete_cart_item'),

    #views from order app
    path('orders/checkout/', order_views.checkout_view, name='checkout_page'),
    path('orders/place-order/', order_views.place_order_view, name='place_order'),
    path('orders/add-address', order_views.add_address_order_view, name='add_address_order'),
        
    path('orders/success/', order_views.order_success_view, name="order_success"),
    path('order/invoice/<int:order_id>/', order_views.view_invoice, name='view_invoice'),
    path('order/invoice/<int:order_id>/download-pdf/', order_views.download_invoice_pdf_view, name='download_invoice_pdf'),
    path('user/orders/', order_views.user_orders_view, name="user_orders"),
    path('user/orders/<str:order_number>/', order_views.user_order_details_view, name="user_order_details"),
    path('user/orders/<str:order_number>/cancel/', order_views.user_cancel_order_view, name="user_cancel_order"),
    path('user/orders/<str:order_number>/return/', order_views.user_return_order_view, name="user_return_order"),
    path('user/orders/<int:order_id>/payment/', order_views.user_pending_order_payment_view, name="user_pending_order_payment"),
    path('user/orders/<str:order_number>/item/<int:item_id>/cancel/', order_views.user_cancel_order_item_view, name="user_cancel_order_item"),
    path('user/orders/<str:order_number>/item/<int:item_id>/return/', order_views.user_return_order_item_view, name="user_return_order_item"),

    path('user/payment/status', order_views.payment_status, name="payment_status"),#razor pay payment url
    path('user/wallet_payment/status', order_views.wallet_payment_status, name="wallet_payment_status"),#razor pay payment url for wallet payment also.
   
   #views from coupon app
    path('orders/apply-coupon/', coupon_views.apply_coupon_view, name='apply_coupon'),
    path('orders/remove-coupon/', coupon_views.remove_coupon_view, name='remove_coupon'),
    

    #views from wishlist app
    path('wishlist/', wishlist_views.wishlist_view, name='wishlist_page'),
    path('wishlist/add/<int:variant_id>', wishlist_views.add_to_wishlist_view, name='add_to_wishlist'),
    path('wishlist/remove/<int:variant_id>', wishlist_views.remove_from_wishlist_view, name='remove_from_wishlist'),

    #views from wallet app
    path('user/wallet/', wallet_views.user_wallet_view, name='user_wallet'),
    
    
]