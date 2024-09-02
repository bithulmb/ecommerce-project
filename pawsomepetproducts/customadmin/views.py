from django.shortcuts import render,redirect
from accounts.models import CustomUser
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from .decorators import superuser_required
from accounts.forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import requests
from accounts.decorators import superuser_required
from orders.models import Order
from product.models import Product_Variant
from category.models import Category
from accounts.models import CustomUser
from django.db.models import Sum, F, Q, Count
from django.utils import timezone
from datetime import timedelta




# Create your views here.

#view function for redirecting to login page
def admin_panel_view(request):
    return redirect('admin_login')


#view funntion for admin login page
@never_cache
def admin_login_view(request):
    
    if request.user.is_authenticated and request.user.is_superadmin:
        return redirect('admin_dashboard')
    
    
    if request.method=='POST':

        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user=authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_superadmin:
                    login(request,user)

                    #for redirecting to the url mentioned in next while logging in
                    url=request.META.get('HTTP_REFERER')
                    try:
                        query=requests.utils.urlparse(url).query
                        params=dict(x.split("=") for x in query.split("&"))
                        if 'next' in params:
                            nextPage=params['next']
                            return redirect(nextPage)
                    except:
                        pass
                    return redirect('admin_dashboard')
                else:
                    messages.error(request,'You are not authorised to access the details')
            else:
                messages.error(request,"Invalid credentials")

        else:
    
            messages.error(request, "Please correct the errors")
    else:
        form = LoginForm()

    return render(request, 'admin/admin_login.html', {'form': form})
       
       
       
     




#view function of dashboard page after logging in
@never_cache
@superuser_required
def admin_dashboard_view(request):

    delivered_orders = Order.objects.filter(status = 'Delivered')
    
    total_order_count = delivered_orders.count()
    
    total_revenue = delivered_orders.aggregate(total = Sum('total_amount'))['total']

    product_count = Product_Variant.objects.filter(is_active=True).count()

    category_count = Category.objects.filter(is_active=True).count()
    
    users_count = CustomUser.objects.filter(is_active = True, is_blocked = False, is_superadmin= False).count()

    context = {
        'total_order_count' : total_order_count,
        'total_revenue' : total_revenue,
        'product_count' : product_count,
        'category_count' : category_count,
        'users_count' : users_count


    }

    return render(request, 'admin/admin_dashboard.html', context)



#view function for logging out admin
@never_cache
def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')



#view function of sales report page after logging in
@never_cache
@superuser_required
def admin_sales_report_view(request):
    
    # Initialize variables to store the filter criteria
    filter_option = request.GET.get('filter', 'overall')  # Default filter is daily
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    orders = Order.objects.filter(status="Delivered", is_ordered = True)
    # Set default query filters based on the selected option
    if filter_option == 'daily':        
        filter_date =timezone.localtime(timezone.now()).date()      
        orders = orders.filter(created_at__date=filter_date).order_by('-created_at')
        
    elif filter_option == 'weekly':        
        filter_date = timezone.now() - timedelta(days=7)
        orders = orders.filter(created_at__gte=filter_date).order_by('-created_at')
    
    elif filter_option == 'monthly':
        filter_date = timezone.now() - timedelta(days=30)
        orders = orders.filter(created_at__gte=filter_date).order_by('-created_at')
    
    elif filter_option == 'custom' and start_date and end_date:
        orders = orders.filter(created_at__range=[start_date, end_date]).order_by('-created_at')
    
    else:
        orders = orders.order_by('-created_at')
        

    # Calculate report details
    sales_count = orders.count()
    total_sales = orders.aggregate(total=Sum('order_total'))['total'] or 0
    total_offer_discount = orders.aggregate(total=Sum('offer_amount'))['total'] or 0
    total_coupon_discount = orders.aggregate(total=Sum('discount_amount'))['total'] or 0 
    total_shipping_charge = orders.aggregate(total = Sum('shipping_charge'))['total'] or 0 
    net_total_revenue = orders.aggregate(total = Sum('total_amount'))['total'] or 0
    

    context = {
        'orders': orders,
        'sales_count': sales_count,
        'total_sales': total_sales,
        'total_offer_discount': total_offer_discount,
        'total_coupon_discount': total_coupon_discount,
        'filter': filter_option,
        'start_date': start_date,
        'end_date': end_date,
        'total_shipping_charge' : total_shipping_charge,
        'net_total_revenue' : net_total_revenue,

    }
 

    return render(request, 'admin/admin_sales_report.html', context)


