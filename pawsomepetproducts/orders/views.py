from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import CartItem,Cart
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Address
from accounts.forms import AddAddressForm
from .models import Order,Payment,OrderProduct
import datetime
from django.http import HttpResponse
from product.models import Product_Variant
from django.contrib import messages
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from accounts.decorators import superuser_required
import razorpay
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


client  = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# Create your views here.

#-------------------------------------admin side views------------------

#view for listing the orders in adminpanel
@superuser_required
@never_cache
def admin_orders_view(request):
    query=request.GET.get('q')
    if query:   #if there is search query
        orders=Order.objects.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(user__email__icontains=query) | Q(order_number__icontains=query))
    else:
        orders=Order.objects.filter(is_ordered=True).order_by('-created_at')
    
    #for pagination
    paginator = Paginator(orders, 8) 
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    


    return render(request,'admin/admin_orders.html', {'orders':orders})


@superuser_required
@never_cache
def admin_order_details_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        messages.success(request, 'Order status updated successfully.')
        return redirect('admin_orders')
    order_items = OrderProduct.objects.filter(order=order)
    payment_details=get_object_or_404(Payment, order=order)
    
    context = {
                'order': order, 
                'order_items': order_items, 
                'payment_details' : payment_details,
               }
    return render(request, 'admin/admin_order_detail.html', context )


# -------------------------------user views-------------------------------
#view function for checkoout page
@login_required(login_url='login_page')
@never_cache
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
@login_required(login_url='login_page')
@never_cache
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
            
            #creating an order instance and saving
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
            # authorize razorpay client with API Keys.
            client  = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            amount = int(grand_total * 100)  # Convert to paisa          
            
            #creating an order instance and saving
            order_instance = Order()
            order_instance.user = current_user
            order_instance.address = Address.objects.get(id=address_id)
            order_instance.total_amount = grand_total
            order_instance.payment_method = "Online"
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
            
            data = { 
                "amount": amount, 
                "currency": "INR", 
                "receipt": order_number,
                "payment_capture": "1",
                 }
            
            
            #create a razor pay order
            razorpay_order=client.order.create(data = data)
            
            order_id=razorpay_order['id']
            order_status=razorpay_order['status']
            context={}


            if order_status == 'created':

                context={
                    'order_id':order_id,
                    'amount': amount,
                    'user': current_user

                    
                }
            # Store the Razorpay order ID  and orderin session
            request.session['razorpay_order_id'] = razorpay_order['id']
            request.session['order_id'] = order_instance.id

            return render(request, 'user_home/payment.html', context=context)

#view function for confirming the status of payment
@csrf_exempt
def payment_status (request) :
    if request.method == "POST":
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)
            
            # payment successful, save payment details
            order_id = request.session.get('order_id')
            order_instance = Order.objects.get(id=order_id)
            #creating an isntance of payment and saving
            payment_instance = Payment(
                user=request.user,
                payment_id=razorpay_payment_id,
                payment_method="Online",
                amount_paid=order_instance.total_amount,
                status="Completed",
            )
            payment_instance.save()
            
            #saving payment instance to order instance
            order_instance.payment = payment_instance
            order_instance.is_ordered = True
            order_instance.save()

            # Clear session
            del request.session['razorpay_order_id']
            del request.session['order_id']

            #getting the items in cart
            cart_items = CartItem.objects.filter(user=request.user)
            
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
           
        except razorpay.errors.SignatureVerificationError:
            return HttpResponseBadRequest()
    return HttpResponseBadRequest()



#view function for adding address in checkout page
@login_required(login_url='login_page')
@never_cache
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
@login_required(login_url='login_page')
@never_cache
def order_success_view(request):
    order = Order.objects.filter(user=request.user).last()
    return render(request,'user_home/order_success.html',{'order':order})

@login_required(login_url='login_page')
@never_cache
def view_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'user_home/invoice.html', {'order': order})




#view function for displaying orders in user profile
@login_required(login_url='login_page')
@never_cache
def user_orders_view(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }

    return render(request,'user_home/user_orders.html',context)

#view function for detailed order view of a order
@login_required(login_url='login_page')
@never_cache
def user_order_details_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    order_items = OrderProduct.objects.filter(order=order)
    payment_details=Payment.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items,
        'payment_details' : payment_details,
    }
    return render(request, 'user_home/user_order_details.html', context)

#view function for cancelling an order
@login_required(login_url='login_page')
@never_cache
def user_cancel_order_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    if request.method == 'POST':
        order.status = 'Cancelled'
        order.save()
        messages.success(request, 'Cancellation Of Order Succesful')
        return redirect('user_orders')
    return render(request, 'user_home/confirm_cancel_order.html',{'order':order})


