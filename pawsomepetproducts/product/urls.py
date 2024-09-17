from django.urls import path

from . import views

urlpatterns = [
    # Adminside views
    # path('',views.admin_products_view, name='admin_products'), #admin side product list page
    # path('add/',views.admin_add_product_view, name='admin_add_product'),
    # path('edit/<int:pk>', views.admin_edit_product_view, name='admin_edit_product'),
    # path('variants/', views.admin_product_variants_view, name = 'admin_product_variants'),
    # path('variants/edit/<int:pk>', views.admin_edit_product_variant_view, name='admin_edit_product_variant'),
    # path('variants/add/',views.admin_add_product_variant_view, name='admin_add_product_variant'),
    # user side views
    # path('products/', views.all_products_view, name='all_products_page'),  #userside all products page
    # path('products/<int:pk>', views.single_product_view, name='single_product_page'),
]
