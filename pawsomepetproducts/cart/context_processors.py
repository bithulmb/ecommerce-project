from .models import Cart, CartItem
from .views import _cart_id


# context processor function for calculating the number of items in cart
def counter(request):
    cart_count = 0
    # if request.user.is_superuser:
    #     return {}
    # else:
    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request))
        # if user is authenticated cart items are filetered based on user id else based on last cartid
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart_items = CartItem.objects.filter(cart=cart[:1])

        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_count = 0
    return dict(cart_count=cart_count)
