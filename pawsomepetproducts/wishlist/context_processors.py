from .models import Wishlist


# context processor function for calculating the number of items in cart
def wishlist_counter(request):
    if request.user.is_authenticated:
        count = Wishlist.objects.filter(user=request.user).count()
    else:
        count = 0
    return dict(wishlist_count=count)
