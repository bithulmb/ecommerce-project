from django.urls import path
from . import views


urlpatterns = [
    
    path('products/', views.all_products_view, name='all_products_page'),
    # path('add/',views.admin_add_pet_type_view, name='admin_add_pet_type'),
    # path('edit/<int:pk>', views.admin_edit_pet_type_view, name='admin_edit_pet_type')
    
]