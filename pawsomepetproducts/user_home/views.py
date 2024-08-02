from django.shortcuts import render, redirect
from product.models import Product_Variant
from django.contrib import messages


# Create your views here.

#View function for displaying home page
def home_view(request):
    product_variants=Product_Variant.objects.all()
    return render(request,'user_home/home.html', {'product_variants': product_variants})

#View function for displaying aboutus page
def about_us_view(request):
    return render(request, 'user_home/about_us.html')

#View function for displaying contact us page
def contact_us_view(request):
    return render(request, 'user_home/contact_us.html')


        
