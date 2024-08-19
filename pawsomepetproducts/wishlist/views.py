
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist
from accounts.models import CustomUser
from product.models import Product_Variant


# Create your views here.

#view function for wishlist page
@login_required(login_url='login_page')
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'user_home/wishlist.html', {'wishlist_items': wishlist_items})



#view function for adding products to wishlist
@login_required(login_url='login_page')
def add_to_wishlist_view(request, variant_id):
    product_variant = get_object_or_404(Product_Variant, id=variant_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product_variant=product_variant)

    #if no object exist, created will be true
    if created:
        messages.success(request, 'Product added to wishlist!')
    #if  already a object exist, created will be false
    else:
        messages.info(request, 'Product is already in your wishlist.')

    return redirect('wishlist_page')

#view function for removing the product from wishlist
@login_required(login_url='login_page')
def remove_from_wishlist_view(request, variant_id):
    product_variant = get_object_or_404(Product_Variant, id=variant_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product_variant=product_variant).first()

    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, 'Product removed from wishlist.')
    else:
        messages.error(request, 'Product was not in your wishlist.')

    return redirect('wishlist_page')