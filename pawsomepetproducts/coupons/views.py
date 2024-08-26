from django.shortcuts import render,redirect
from .forms import ApplyCouponForm
from .models import Coupon
from cart.models import CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.http import Http404
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from accounts.models import Address
from django.contrib import messages
from django.views.decorators.http import require_POST

# Create your views here.

#view function for applying coupon
@login_required(login_url='login_page')
@never_cache
@require_POST
def apply_coupon_view(request):
    
    total,quantity,grand_total=0,0,0
    discounted_total=None
    cart_items=None
    try:
        cart_items=CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.variant.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        if total>=500:
            shipping_charge=0
        else:
            shipping_charge = 100
        grand_total = total + shipping_charge
        
    except ObjectDoesNotExist:
        raise Http404
    addresses=Address.objects.filter(user=request.user)
    context={
        'total':total,
        'quantity':quantity,
        'cart_items' :cart_items,
        'shipping_charge':shipping_charge,
        'grand_total': grand_total,
        'addresses' :  addresses,
        
    }
    url = request.META.get('HTTP_REFERER')
    form = ApplyCouponForm(request.POST or None)
    if form.is_valid():
        code = form.cleaned_data.get('code')
        
        try:
            coupon = Coupon.objects.get(code=code, active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
            #checking the order amount is greater than the minumum ordr amount
            if grand_total >= coupon.minimum_order_amount: 

                discount = round(grand_total*coupon.discount/100, 2) # calculating the discount and rounding off the decimal value to 2 points.
                # checking if the discount amount less than the maximum discount limit
                if coupon.maximum_discount_limit:
                    if (discount) > coupon.maximum_discount_limit:            
                        discount = coupon.maximum_discount_limit
                        
                discounted_total = grand_total-discount
                context['coupon']=coupon
                context['discounted_total']=discounted_total
                context['discount'] = discount
                
                request.session['coupon_code'] = coupon.code
                request.session['discount'] = float(discount)
                messages.success(request,"Coupon Applied Succesfully")
                return render(request, 'user_home/checkout.html', context)
                
            else:
                 print("else block")
                 messages.error(request,f"Coupon is only valid for orders above ₹ {coupon.minimum_order_amount} ")
                 context['form']=form
                 return redirect(url)
                

        except Coupon.DoesNotExist:
            messages.error(request,"Coupon is invalid or expired")
            context['form']=form
            # return render(request, 'user_home/checkout.html', context)
            return redirect(url)

            
    context['form']=form
    return redirect(url)


#view function for removing applied coupon
@login_required
@never_cache
def remove_coupon_view(request):
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
    if 'discount' in request.session:
        del request.session['discount']
   
    messages.error(request,"Applied Coupon removed")
    return redirect('checkout_page')