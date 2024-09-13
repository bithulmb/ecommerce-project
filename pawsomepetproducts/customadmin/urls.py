from django.urls import path, include
from . import views
from accounts import views as account_views
from category import views as category_views
from pet_type import views as pet_type_views
from product import views as product_views
from orders import views as order_views
from coupons import views as coupon_views
from offers import views as offers_views


#url patterns in the admin panel
urlpatterns = [
    path('admin-panel/',views.admin_panel_view),
    path('admin-panel/login/',views.admin_login_view, name='admin_login'),
    path('admin-panel/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-panel/logout/', views.admin_logout_view, name='admin_logout'),
    path('admin-panel/sales-report/', views.admin_sales_report_view, name='admin_sales_report'),
    path('admin-panel/get-sales-data/', views.get_sales_data, name='get_sales_data'),
    path('admin-panel/get-category-sales-data/', views.get_category_sales_data, name='get_category_sales_data'),
    path('admin-panel/get-category-count-data/', views.get_category_count_data, name='get_category_count_data'),
    
    #list of users from accounts app
    path('admin-panel/users/', account_views.admin_users_view, name='admin_users'),
    path('admin-panel/users/edit/<int:pk>', account_views.admin_edit_user_view, name='admin_edit_user'),

    #category related urls from category app
    path('admin-panel/category/', category_views.admin_category_view, name='admin_category'),
    path('admin-panel/category/add/',category_views.admin_add_category_view, name='admin_add_category'),
    path('admin-panel/category/edit/<int:pk>', category_views.admin_edit_category_view, name='admin_edit_category'),

    #PetType management urls from pet_type app
    path('admin-panel/pet-type/',pet_type_views.admin_pet_type_view, name='admin_pet_type'),
    path('admin-panel/pet-type/add/',pet_type_views.admin_add_pet_type_view, name='admin_add_pet_type'),
    path('admin-panel/pet-type/edit/<int:pk>', pet_type_views.admin_edit_pet_type_view, name='admin_edit_pet_type'),

    #Product and variant management urls from product app
    path('admin-panel/products/',product_views.admin_products_view, name='admin_products'), #admin side product list page
    path('admin-panel/products/add/',product_views.admin_add_product_view, name='admin_add_product'),
    path('admin-panel/products/edit/<int:pk>', product_views.admin_edit_product_view, name='admin_edit_product'),
    path('admin-panel/variants/', product_views.admin_product_variants_view, name = 'admin_product_variants'),
    path('admin-panel/variants/edit/<int:pk>', product_views.admin_edit_product_variant_view, name='admin_edit_product_variant'),
    path('admin-panel/variants/add/', product_views.admin_add_product_variant_view, name='admin_add_product_variant'),
    path('admin-panel/variants/<int:variant_id>/image', product_views.admin_add_edit_product_images_view, name='admin_add_edit_product_images'),

    # order related urls from order app
    path('admin-panel/orders/', order_views.admin_orders_view, name='admin_orders'),
    path('admin-panel/orders/<int:order_id>/', order_views.admin_order_details_view, name='admin_order_details'),
    path('admin-panel/orders/product-return', order_views.admin_order_product_return_view, name='admin_order_product_return'),
   path('admin-panel/orders/product-return/<int:order_item_id>/approve', order_views.admin_order_product_return_approve_view, name='admin_order_product_return_approve'),

    #coupon related urls from coupon app
    path('admin-panel/coupons/', coupon_views.admin_coupons_view, name='admin_coupons'),
    path('admin-panel/coupons/add', coupon_views.admin_add_coupon_view, name='admin_add_coupon'),
    path('admin-panel/coupons/<int:coupon_id>/edit', coupon_views.admin_edit_coupon_view, name='admin_edit_coupon'),

    #offer related urls from the offers app
    path('admin-panel/offers/', offers_views.admin_offers_view, name='admin_offers'),
    path('admin-panel/offers/product/', offers_views.admin_product_offers_view, name='admin_product_offers'),
    path('admin-panel/offers/product/add', offers_views.admin_add_product_offer_view, name='admin_add_product_offer'),
    path('admin-panel/offers/product/<int:product_offer_id>/edit', offers_views.admin_edit_product_offer_view, name='admin_edit_product_offer'),
    path('admin-panel/offers/category', offers_views.admin_category_offers_view, name='admin_category_offers'),
    path('admin-panel/offers/category/add', offers_views.admin_add_category_offer_view, name='admin_add_category_offer'),
    path('admin-panel/offers/category/<int:category_offer_id>/edit', offers_views.admin_edit_category_offer_view, name='admin_edit_category_offer'),


]




    