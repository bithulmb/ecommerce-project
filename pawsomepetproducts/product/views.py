from django.shortcuts import render,redirect,get_object_or_404
from .models import Product_Variant
from .models import Product
from pet_type.models import PetType
from category.models import Category
from .forms import AddProductForm,AddProductVariantForm,AddProductImages
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from cart.models import CartItem
from cart.views import _cart_id
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
#-------------------------admin side views----------------------------------

#view function for listing the products
@never_cache
@staff_member_required(login_url="admin_login")
def admin_products_view(request):
    query=request.GET.get('q')
    if query:
        products=Product.objects.filter(name__icontains=query)
    else:
        products=Product.objects.all()
    return render(request, 'admin/admin_products.html', {'products': products})

#view fucntion for editing the product 
@never_cache
@staff_member_required(login_url="admin_login")
def admin_edit_product_view(request,pk):
    object=Product.objects.get(id=pk)
    if request.method == 'POST':
        form=AddProductForm(request.POST, instance = object)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form=AddProductForm(instance = object)
    return render(request, 'admin/admin_edit_product.html', {'form':form})

#view function for adding new product
@never_cache
@staff_member_required(login_url="admin_login")
def admin_add_product_view(request):
    if request.method == 'POST':        
        form=AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form=AddProductForm()
    return render(request, 'admin/admin_add_product.html', {'form':form})


#view fucntion for listing product variants
@never_cache
@staff_member_required(login_url="admin_login")
def admin_product_variants_view(request):
    query=request.GET.get('q')
    if query:
        product_variants=Product_Variant.objects.filter(name__icontains=query)
    else:
        product_variants=Product_Variant.objects.all()
    return render(request, 'admin/admin_product_variants.html', {'product_variants': product_variants})

#view fucntion for editing the product variant 
@never_cache
@staff_member_required(login_url="admin_login")
def admin_edit_product_variant_view(request,pk):
    object=Product_Variant.objects.get(id=pk)
    if request.method == 'POST':
        form=AddProductVariantForm(request.POST, instance = object)
        if form.is_valid():
            form.save()
            return redirect('admin_product_variants')
    else:
        form=AddProductVariantForm(instance = object)
    return render(request, 'admin/admin_edit_product_variant.html', {'form':form})


#view function for adding new product variant
@never_cache
@staff_member_required(login_url="admin_login")
def admin_add_product_variant_view(request):
    if request.method == 'POST':        
        form=AddProductVariantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_product_variants')
    else:
        form=AddProductVariantForm()
    return render(request, 'admin/admin_add_product_variant.html', {'form':form})

#view for adding images for product variants
@staff_member_required(login_url="admin_login")
def admin_add_product_images_view(request, variant_id):
    variant = get_object_or_404(Product_Variant, id=variant_id)
    
    if request.method == 'POST':
        form = AddProductImages(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.product_variant = variant
            image.save()
            return redirect('admin_product_variants')  # Redirect to the variants page
    else:
        form = AddProductImages()
    
    return render(request, 'admin/add_product_images.html', {'form': form, 'variant': variant})

#-------------------------user side views----------------------------------

#view function for all products page
def all_products_view(request):
    pet_type_id=request.GET.get('pet_type')
    category_id=request.GET.get('category')
    sort_by = request.GET.get('sort_by')

    products = Product_Variant.objects.filter(is_active=True).order_by('id')

    if pet_type_id:
        products = Product_Variant.objects.filter(is_active=True).filter(product_name__pet_type__id=pet_type_id)
    if category_id:
         products = Product_Variant.objects.filter(is_active=True).filter(product_name__category__id=category_id)

    if sort_by=='price_low_high':
        products=products.order_by('price')
    elif sort_by=='price_high_low':
        products=products.order_by('-price')
    elif sort_by=='az':
        products=products.order_by('product_name__name')
    elif sort_by=='za':
        products=products.order_by('-product_name__name')

    pet_types= PetType.objects.filter(is_active=True)
    categories=Category.objects.filter(is_active=True)

    #for paginator
    paginator=Paginator(products,6)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)

    context={
        'products': paged_products,
        'pet_types' : pet_types,
        'categories' : categories,
        'count' :products.count()  
    }
    return render(request, 'user_home/all_products.html', context)


#view function for viewing single product
def single_product_view(request, pk):
    product_variant = Product_Variant.objects.get(id=pk)
    all_variants = Product_Variant.objects.filter(product_name = product_variant.product_name)
    in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),variant=product_variant).exists() #checking if the item is already added to the cart   
    context = {
        'product_variant': product_variant,
        'all_variants': all_variants,
        'in_cart'   : in_cart
    }
    return render(request, 'user_home/single_product.html', context)