from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache

from product.models import Product_Variant

# Create your views here.


# View function for displaying home page
@never_cache
def home_view(request):
    product_variants = Product_Variant.objects.all()[:8]
    return render(
        request, "user_home/home.html", {"product_variants": product_variants}
    )


# View function for displaying aboutus page
@never_cache
def about_us_view(request):
    return render(request, "user_home/about_us.html")


# View function for displaying contact us page
@never_cache
def contact_us_view(request):
    return render(request, "user_home/contact_us.html")
