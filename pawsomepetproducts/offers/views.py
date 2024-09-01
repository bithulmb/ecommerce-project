from django.shortcuts import render, redirect
from accounts.decorators import superuser_required
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.views.decorators.cache import never_cache
from .models import CategoryOffer,ProductVariantOffer
from .forms import AddCategoryOffer, AddProductOffer
from django.contrib import messages

# Create your views here.


# ------------------------------------admin side views------------------------------

def admin_offers_view(request):
    pass



#view for admin side product offer management
@superuser_required
@never_cache
def admin_product_offers_view(request):
    query=request.GET.get('q')
    if query:
        offers=ProductVariantOffer.objects.filter(product__product_name__name__icontains=query)
    else:
        offers=ProductVariantOffer.objects.all().order_by('-id')
    
    #for pagination
    paginator = Paginator(offers, 8) 
    page = request.GET.get('page')
    try:
        offers = paginator.page(page)
    except PageNotAnInteger:
        offers = paginator.page(1)
    except EmptyPage:
        offers = paginator.page(paginator.num_pages)


    return render(request, 'admin/admin_product_offers.html', {'offers': offers})



#view function for adding new product offer
@superuser_required
@never_cache
def admin_add_product_offer_view(request):
    if request.method == 'POST':        
        form=AddProductOffer(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Offer added succesfully")
            return redirect('admin_product_offers')
    else:
        form=AddProductOffer()
    return render(request, 'admin/admin_add_product_offer.html', {'form':form})



#view fucntion for editing the product offer
@superuser_required
@never_cache
def admin_edit_product_offer_view(request, product_offer_id):
    object=ProductVariantOffer.objects.get(id=product_offer_id)
    if request.method == 'POST':
        form=AddProductOffer(request.POST, instance = object)
        if form.is_valid():
            form.save()
            messages.success(request," Product Offer details updated succesfully")
            return redirect('admin_product_offers')
    else:
        form=AddProductOffer(instance = object)
    return render(request, 'admin/admin_edit_product_offer.html', {'form':form})



#view for admin side category offer management
@superuser_required
@never_cache
def admin_category_offers_view(request):
    query=request.GET.get('q')
    if query:
        offers=CategoryOffer.objects.filter(category__name__icontains=query)
    else:
        offers=CategoryOffer.objects.all().order_by('-id')
    
    #for pagination
    paginator = Paginator(offers, 8) 
    page = request.GET.get('page')
    try:
        offers = paginator.page(page)
    except PageNotAnInteger:
        offers = paginator.page(1)
    except EmptyPage:
        offers = paginator.page(paginator.num_pages)


    return render(request, 'admin/admin_category_offers.html', {'offers': offers})


#view function for adding new category offer
@superuser_required
@never_cache
def admin_add_category_offer_view(request):
    if request.method == 'POST':        
        form=AddCategoryOffer(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Offer added succesfully")
            return redirect('admin_category_offers')
    else:
        form=AddCategoryOffer()
    return render(request, 'admin/admin_add_category_offer.html', {'form':form})



#view fucntion for editing the category offer
@superuser_required
@never_cache
def admin_edit_category_offer_view(request, category_offer_id):
    object=CategoryOffer.objects.get(id=category_offer_id)
    if request.method == 'POST':
        form=AddCategoryOffer(request.POST, instance = object)
        if form.is_valid():
            form.save()
            messages.success(request," Category Offer details updated succesfully")
            return redirect('admin_category_offers')
    else:
        form=AddCategoryOffer(instance = object)
    return render(request, 'admin/admin_edit_category_offer.html', {'form':form})