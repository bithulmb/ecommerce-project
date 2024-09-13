from django.shortcuts import render,redirect
from product.models import Product_Variant
from.models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views.decorators.cache import never_cache


# Create your views here.

#private function for getting the cartid from the session
def _cart_id(request):
    cart=request.session.session_key #getting the session key and storing it as cartid
    if not cart:
        cart=request.session.create()  #if no session , creating a a session and storing it
    return cart

#view function to add products to cart
def add_to_cart_view(request, variant_id):
    variant=Product_Variant.objects.get(id=variant_id)

    if request.user.is_authenticated:
        # If the user is authenticated, check for a CartItem associated with the user
        try:
            cart_item = CartItem.objects.get(variant=variant, user=request.user)
            if cart_item.quantity<variant.stock:          
                if cart_item.quantity<3:
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    messages.error(request,"Maximum 3 quantity per product is allowed for a user")
                    return redirect('cart_page')
            else:
                messages.error(request,"No more stocks available")
                return redirect('cart_page')
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(variant=variant, quantity=1, user=request.user)
            cart_item.save()
    else:
         # If the user is not authenticated, use the session-based cart
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(cart_id = _cart_id(request))
        cart.save()

        try:
            cart_item=CartItem.objects.get(variant=variant, cart=cart)
            if cart_item.quantity<variant.stock:          
                if cart_item.quantity<3:
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    messages.error(request,"Maximum 3 quantity per product is allowed for a user")
                    return redirect('cart_page')
            else:
                messages.error(request,"No more stocks available")
                return redirect('cart_page')

        except CartItem.DoesNotExist:
            cart_item=CartItem.objects.create(variant=variant, quantity=1, cart=cart,)
            cart_item.save()
            
    return redirect('cart_page')


#view function for decrementing products from cart
def remove_from_cart_view(request, variant_id):
    
    variant=Product_Variant.objects.get(id=variant_id)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(variant=variant, user=request.user)
            
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))    
        cart_item=CartItem.objects.get(variant=variant, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_page')

#view function for removing complete cart item
def delete_cart_item_view(request, variant_id):
    variant=Product_Variant.objects.get(id=variant_id)
    #if user is authenticated cart items are filetered based on user id else based on last cartid
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(variant=variant, user=request.user)
            
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))    
        cart_item=CartItem.objects.get(variant=variant, cart=cart)
        
    
    cart_item.delete()
    return redirect('cart_page')


#view function for displaying cart 
def cart_view(request, total=0, quantity=0, cart_items=None):
    shipping_charge=100
    grand_total=0
    offer_discount = 0
    try:
          #if user is authenticated cart items are filetered based on user id else based on last cartid
        if request.user.is_authenticated:
             cart_items=CartItem.objects.filter(user=request.user, is_active=True).order_by('id')
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart, is_active=True).order_by('id')
        
        for cart_item in cart_items:
            total += (cart_item.variant.price * cart_item.quantity)
            quantity += cart_item.quantity
            offer_discount += (cart_item.variant.discount_amount() * cart_item.quantity)
            
        
        if total>=500:
            shipping_charge=0
        grand_total = total + shipping_charge - offer_discount     
    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items' :cart_items,
        'shipping_charge':shipping_charge,
        'grand_total': grand_total, 
        'offer_discount' : offer_discount,   
         }
    return render(request,'user_home/cart.html',context)





