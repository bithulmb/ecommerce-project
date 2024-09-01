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
from accounts.decorators import superuser_required
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from .forms import AddCouponForm
from wallet.models import Wallet



# Create your views here.

# --------------------------------------user side views--------------------------------------


#view function for applying coupon
@login_required(login_url='login_page')
@never_cache
@require_POST
def apply_coupon_view(request):
    
    total,quantity,grand_total,offer_discount=0,0,0,0
    discounted_total=None
    cart_items=None
    try:
        cart_items=CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.variant.price * cart_item.quantity)
            quantity += cart_item.quantity
            offer_discount += (cart_item.variant.discount_amount() * cart_item.quantity)
        
        if total>=500:
            shipping_charge=0
        else:
            shipping_charge = 100
        grand_total = total + shipping_charge - offer_discount
        
    except ObjectDoesNotExist:
        raise Http404
    addresses=Address.objects.filter(user=request.user)
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    context={
        'total':total,
        'quantity':quantity,
        'cart_items' :cart_items,
        'shipping_charge':shipping_charge,
        'grand_total': grand_total,
        'addresses' :  addresses,
        'wallet' : wallet,
        'offer_discount' : offer_discount,  
        
    }
    url = request.META.get('HTTP_REFERER')
    form = ApplyCouponForm(request.POST or None)
    if form.is_valid():
        code = form.cleaned_data.get('code')
        
        try:
            coupon = Coupon.objects.get(code=code, active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
            #checking the order amount is greater than the minumum ordr amount
            if grand_total >= coupon.minimum_order_amount: 

                discount = round(grand_total*coupon.discount_percent/100, 2) # calculating the discount and rounding off the decimal value to 2 points.
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



# -----------------------------------------------------admin side views-------------------------------------------------



#view for admin side coupon management
@superuser_required
@never_cache
def admin_coupons_view(request):
    query=request.GET.get('q')
    if query:
        coupons=Coupon.objects.filter(code__icontains=query)
    else:
        coupons=Coupon.objects.all().order_by('-id')
    
    #for pagination
    paginator = Paginator(coupons, 8) 
    page = request.GET.get('page')
    try:
        coupons = paginator.page(page)
    except PageNotAnInteger:
        coupons = paginator.page(1)
    except EmptyPage:
        coupons = paginator.page(paginator.num_pages)


    return render(request, 'admin/admin_coupons.html', {'coupons': coupons})

#view function for adding new coupon
@superuser_required
@never_cache
def admin_add_coupon_view(request):
    if request.method == 'POST':        
        form=AddCouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon added succesfully")
            return redirect('admin_coupons')
    else:
        form=AddCouponForm()
    return render(request, 'admin/admin_add_coupon.html', {'form':form})



#view fucntion for editing the coupon 
@superuser_required
@never_cache
def admin_edit_coupon_view(request,coupon_id):
    object=Coupon.objects.get(id=coupon_id)
    if request.method == 'POST':
        form=AddCouponForm(request.POST, instance = object)
        if form.is_valid():
            form.save()
            messages.success(request," Coupon details updated succesfully")
            return redirect('admin_coupons')
    else:
        form=AddCouponForm(instance = object)
    return render(request, 'admin/admin_edit_coupon.html', {'form':form})