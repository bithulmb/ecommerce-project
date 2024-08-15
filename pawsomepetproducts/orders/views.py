from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem,Cart
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Address
from accounts.forms import AddAddressForm
from .models import Order,Payment,OrderProduct
import datetime
from django.http import HttpResponse
from product.models import Product_Variant

# Create your views here.


# -------------------------------user views-------------------------------
#view function for checkoout page
@login_required(login_url='login_page')
def checkout_view(request, total=0, quantity=0, cart_items=None):
    shipping_charge=100
    grand_total=0
    try:
        cart_items=CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.variant.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        if total>=500:
            shipping_charge=0
        grand_total = total + shipping_charge
        
    except ObjectDoesNotExist:
        pass
    addresses=Address.objects.filter(user=request.user)
    context={
        'total':total,
        'quantity':quantity,
        'cart_items' :cart_items,
        'shipping_charge':shipping_charge,
        'grand_total': grand_total,
        'addresses' :  addresses,
        
    }
    return render(request,'user_home/checkout.html', context)

#view function for placing order
def place_order_view(request):
    
    current_user=request.user

   
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    
     #if cart items is zero, redirect user to cart page
    if cart_count<=0:
        return redirect('cart_page')
    
    quantity=0
    total=0
    shipping_charge=100
    grand_total=0
    for cart_item in cart_items:
            total += (cart_item.variant.price * cart_item.quantity)
            quantity += cart_item.quantity
        
    if total>=500:
        shipping_charge=0
    grand_total = total + shipping_charge

    if request.method =='POST':
        address_id = request.POST.get('address_id')
        payment_method = request.POST.get('payment_method')

        #if the user has selected cash on delivery option in payment method
        if payment_method=="cash_on_delivery":
            address = Address.objects.get(id=address_id)
            order_instance = Order()
            order_instance.user=current_user
            order_instance.address=address
            order_instance.total_amount=grand_total
            order_instance.payment_method="Cash On Delivery"
            
            order_instance.save()
            
            # Generate order number
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%y%m%d")
            order_number = current_date + str(order_instance.id)
            order_instance.order_number = order_number
            order_instance.save()

            #creating an instance of payment and saving
            payment_instance = Payment(
                    user=current_user,
                    payment_id=order_number,
                    payment_method="Cash On Delivery",
                    amount_paid=grand_total,
                    status="Pending",
                )
            payment_instance.save()
            
            #saving the payment method to order instance
            order_instance.payment=payment_instance
            order_instance.is_ordered=True
            order_instance.save()
            
            #move the cart items to order product table    
            for item in cart_items:
                order_product_instance=OrderProduct()
                order_product_instance.order=order_instance
                order_product_instance.payment=payment_instance
                order_product_instance.product=item.variant
                order_product_instance.quantity=item.quantity
                order_product_instance.product_price=item.variant.price
                order_product_instance.save() 

            #reduce the number of stock of product
                product=Product_Variant.objects.get(id=item.variant.id)
                product.stock -= item.quantity
                product.save()

            #clearing the cart of the user
            cart_items.delete()


            return redirect('order_success')
        
        if payment_method=="online":
            pass



    

#view function for adding address in checkout page
def add_address_order_view(request):

    if request.method == 'POST':
        form = AddAddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user  # Assign the logged-in user to the address
            new_address.save()
            return redirect('checkout_page')  # Redirect to the cart page after adding the address
    else:
        form = AddAddressForm()
    return render(request, 'user_home/add_address_order.html', {'form': form})


#view function for displaying order success page
def order_success_view(request):
    return render(request,'user_home/order_success.html')


def order_payment_view(request):
    return render(request,'user_home/payment.html')


#view function for displaying orders in user profile
def user_orders_view(request):
    return render(request,'user_home/user_orders.html')