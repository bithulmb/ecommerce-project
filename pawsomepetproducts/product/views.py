from django.shortcuts import render
from .models import Product_Variant

# Create your views here.


def all_products_view(request):
    products=Product_Variant.objects.all()
    return render(request, 'user_home/all_products.html', {'products': products})