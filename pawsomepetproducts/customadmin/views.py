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
from orders.models import Order,OrderProduct
from product.models import Product_Variant
from category.models import Category
from accounts.models import CustomUser
from django.db.models import Sum, F, Q, Count
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.db.models.functions import ExtractMonth, ExtractWeek, ExtractDay
import calendar
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth




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
    
    delivered_order_count = delivered_orders.count()
    
    total_revenue = delivered_orders.aggregate(total = Sum('total_amount'))['total']

    product_count = Product_Variant.objects.filter(is_active=True).count()

    category_count = Category.objects.filter(is_active=True).count()
    
    users_count = CustomUser.objects.filter(is_active = True, is_blocked = False, is_superadmin= False).count()

    processing_orders_count = Order.objects.filter(status = "Processing", is_ordered = True).count()
    
    shipped_orders_count = Order.objects.filter(status = "Shipped", is_ordered = True).count()

    cancelled_orders_count = Order.objects.filter(status = "Cancelled", is_ordered = True).count()   
    
    # Top 10 best-selling products
   
    top_products = (
        OrderProduct.objects.filter(order__status = "Delivered")
        .values('product__product_name__name','product__size')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')[:10]
    )

    # Top 10 best-selling categories
    top_categories = (
        OrderProduct.objects.filter(order__status = "Delivered")
        .values('product__product_name__category__name')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')[:10]
    )
    

    context = {
        'total_revenue' : total_revenue,
        'product_count' : product_count,
        'category_count' : category_count,
        'users_count' : users_count,
        'top_products': top_products,
        'top_categories': top_categories,
        'delivered_order_count' : delivered_order_count,
        'processing_orders_count' : processing_orders_count,
        'shipped_orders_count' : shipped_orders_count,
        'cancelled_orders_count' :cancelled_orders_count





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
    cancelled_orders = Order.objects.filter(status = "Cancelled")

    # Set default query filters based on the selected option
    if filter_option == 'daily':        
        filter_date =timezone.localtime(timezone.now()).date()      
        orders = orders.filter(created_at__date=filter_date).order_by('-created_at')
        cancelled_orders = cancelled_orders.filter(created_at__date=filter_date).order_by('-created_at')
    
    elif filter_option == 'weekly':        
        filter_date = timezone.now() - timedelta(days=7)
        orders = orders.filter(created_at__gte=filter_date).order_by('-created_at')
        cancelled_orders = cancelled_orders.filter(created_at__gte=filter_date).order_by('-created_at')
    
    elif filter_option == 'monthly':
        filter_date = timezone.now() - timedelta(days=30)
        orders = orders.filter(created_at__gte=filter_date).order_by('-created_at')
        cancelled_orders = cancelled_orders.filter(created_at__gte=filter_date).order_by('-created_at')

    elif filter_option == 'custom' and start_date and end_date:
        orders = orders.filter(created_at__range=[start_date, end_date]).order_by('-created_at')
        cancelled_orders = cancelled_orders.filter(created_at__range=[start_date, end_date]).order_by('-created_at')
    else:
        orders = orders.order_by('-created_at')
        

    # Calculate report details
    sales_count = orders.count()
    total_sales = orders.aggregate(total=Sum('order_total'))['total'] or 0
    total_offer_discount = orders.aggregate(total=Sum('offer_amount'))['total'] or 0
    total_coupon_discount = orders.aggregate(total=Sum('discount_amount'))['total'] or 0 
    total_shipping_charge = orders.aggregate(total = Sum('shipping_charge'))['total'] or 0 
    net_total_revenue = orders.aggregate(total = Sum('total_amount'))['total'] or 0
    cancelled_orders_count = cancelled_orders.count() 
   

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
        'cancelled_orders_count' : cancelled_orders_count,
     

    }
 

    return render(request, 'admin/admin_sales_report.html', context)




@require_GET
def get_sales_data(request):
    filter_type = request.GET.get('filter', 'weekly')  # Default to weekly if no filter is provided
    now = timezone.localtime(timezone.now())
    
    orders = Order.objects.filter(status = "Delivered")

    if filter_type == 'yearly':
        # Group by month for the current year
        sales = (
           orders.filter(created_at__year=now.year)
            .annotate(period=TruncMonth('created_at'))
            .values('period')
            .annotate(total_sales=Sum('total_amount'))
            .order_by('period')
        )
        labels = [calendar.month_name[i] for i in range(1, 13)]
        period_map = {now.replace(month=i, day=1).date(): 0 for i in range(1, 13)}

    elif filter_type == 'monthly':
    # Group by week for the current month
        start_date = now.replace(day=1)  # First day of the current month
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)  # Last day of the current month
        sales = (
            orders.filter(created_at__range=(start_date, end_date))
            .annotate(period=TruncWeek('created_at'))  # Group by week
            .values('period')
            .annotate(total_sales=Sum('total_amount'))
            .order_by('period')
        )
        
        
        # Create labels and initialize period_map for each week
        labels = []
        period_map = {}
        current = start_date
        
        while current <= end_date:
            # Calculate the end of the week period
            week_end = min(current + timedelta(days=6), end_date)
            
            # Create label for the week
            label = f"{current.strftime('%d %b')} - {week_end.strftime('%d %b')}"
            labels.append(label)
            
            # Initialize period_map with the exact start dates that match TruncWeek results
            period_map[current] = 0  
            current += timedelta(days=7)  # Move to the next week

        # Update period_map with actual sales data
        for sale in sales:
            period_key = sale['period']
            
            # Ensure period_key aligns with period_map by converting datetime to date if necessary
            if isinstance(period_key, timezone.datetime):
                period_key = period_key.date()  
            
            # Adjust matching by aligning the exact start dates of weeks
            for week_start in period_map.keys():
                week_end = week_start + timedelta(days=6)
                # Check if period_key falls within this week range
                if week_start.date() <= period_key <= week_end.date():
                    period_map[week_start] = float(sale['total_sales'])

        # Ensure data aligns with labels
        data = [period_map[key] for key in sorted(period_map.keys())]
        print(data)
        return JsonResponse({
        'labels': labels,
        'data': data,
        })

        
    else:  # weekly
        # Group by day for the last 7 days
        end_date = now.date()
        start_date = end_date - timedelta(days=6)
        sales = (
            orders.filter(created_at__range=(start_date, end_date + timedelta(days=1)))
            .annotate(period=TruncDate('created_at'))
            .values('period')
            .annotate(total_sales=Sum('total_amount'))
            .order_by('period')
        )
        labels = [(start_date + timedelta(days=i)).strftime('%a, %d %b') for i in range(7)]
        period_map = {start_date + timedelta(days=i): 0 for i in range(7)}
        
    # Update period_map with actual sales data
    
    for sale in sales:
        # Correctly handle period for different filters
        period_key = sale['period']
    
        if isinstance(period_key, timezone.datetime):
            # Handling datetime objects
            period_key = period_key.date()

        if period_key in period_map:
            
            period_map[period_key] = float(sale['total_sales'])
    
    # Ensure data aligns with labels
    data = [period_map[key] for key in sorted(period_map.keys())]
    
    return JsonResponse({
        'labels': labels,
        'data': data,
    })

