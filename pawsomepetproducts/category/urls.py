from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin_category_view, name='admin_category'),
    path('add/',views.admin_add_category_view, name='admin_add_category'),
    path('edit/<int:pk>', views.admin_edit_category_view, name='admin_edit_category')
   
    
]