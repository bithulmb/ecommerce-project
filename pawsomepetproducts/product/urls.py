from django.urls import path
from . import views


urlpatterns = [
    
    path('products/', views.all_products_view, name='all_products_page'),  #userside all products page
    path('',views.admin_products_view, name='admin_products'), #admin side product list page
    path('add/',views.admin_add_product_view, name='admin_add_product'),
    path('edit/<int:pk>', views.admin_edit_product_view, name='admin_edit_product')
    
]