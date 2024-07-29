from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_pet_type_view, name='admin_pet_type'),
    path('add/',views.admin_add_pet_type_view, name='admin_add_pet_type'),
    path('edit/<int:pk>', views.admin_edit_pet_type_view, name='admin_edit_pet_type')
    
]