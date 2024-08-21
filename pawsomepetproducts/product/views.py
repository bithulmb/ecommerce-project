from django.shortcuts import render,redirect,get_object_or_404
from .models import Product_Variant,Product_Images
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
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
import base64
from wishlist.models import Wishlist


# Create your views here.
#-------------------------admin side views----------------------------------

#view function for listing the products
@staff_member_required(login_url="admin_login")
@never_cache
def admin_products_view(request):
    query=request.GET.get('q')
    if query:
        products=Product.objects.filter(name__icontains=query)
    else:
        products=Product.objects.all()
    return render(request, 'admin/admin_products.html', {'products': products})

#view fucntion for editing the product 
@staff_member_required(login_url="admin_login")
@never_cache
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
@staff_member_required(login_url="admin_login")
@never_cache
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
@staff_member_required(login_url="admin_login")
@never_cache
def admin_product_variants_view(request):
    query=request.GET.get('q')
    if query:
        product_variants=Product_Variant.objects.filter(name__icontains=query)
    else:
        product_variants=Product_Variant.objects.all()
    return render(request, 'admin/admin_product_variants.html', {'product_variants': product_variants})

#view fucntion for editing the product variant 
@staff_member_required(login_url="admin_login")
@never_cache
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
@staff_member_required(login_url="admin_login")
@never_cache
def admin_add_product_variant_view(request):
    if request.method == 'POST':        
        form=AddProductVariantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_product_variants')
    else:
        form=AddProductVariantForm()
    return render(request, 'admin/admin_add_product_variant.html', {'form':form})

#view for adding images and editing images for product variants
@staff_member_required(login_url="admin_login") 
@never_cache  
def admin_add_edit_product_images_view(request, variant_id):
    variant = get_object_or_404(Product_Variant, id=variant_id)
    
    if request.method == 'POST':
        if 'delete_image' in request.POST:
            image_id = request.POST.get('image_id')
            Product_Images.objects.filter(id=image_id).delete()
            messages.success(request, 'Image deleted successfully.')
            return redirect('admin_add_edit_product_images', variant_id=variant_id)
        else:
            images = request.FILES.get('images')
           
            Product_Images.objects.create(product_variant=variant, images=images)
            messages.success(request, 'Image added successfully.')
            return redirect('admin_add_edit_product_images', variant_id=variant_id)
    else:
        pass
    
    images = variant.images.all()
    
    return render(request, 'admin/add_edit_product_images.html', {
        
        'variant': variant,
        'images': images
    })


#-------------------------user side views----------------------------------

#view function for all products page
@never_cache
def all_products_view(request):
    pet_type_ids = request.GET.getlist('pet_type')
    category_ids = request.GET.getlist('category')
    sort_by = request.GET.get('sort_by')
   
    products = Product_Variant.objects.filter(is_active=True)

    if pet_type_ids:
        products = products.filter(product_name__pet_type__id__in=pet_type_ids)
    if category_ids:
        products = products.filter(product_name__category__id__in=category_ids)
        
    
    
    if sort_by=='price_low_high':        
        products=products.order_by('price')
    elif sort_by=='price_high_low':
        products=products.order_by('-price')
    elif sort_by=='az':
        products=products.order_by('product_name__name')
    elif sort_by=='za':
        products=products.order_by('-product_name__name')

   

    #for paginator
   
    paginator=Paginator(products,9)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)

    context={
        'products': paged_products,
        'pet_types' : PetType.objects.filter(is_active=True),
        'categories' : Category.objects.filter(is_active=True),
        'count' :products.count(),
        'selected_pet_types': pet_type_ids,
        'selected_categories': category_ids, 
    }


    return render(request, 'user_home/all_products.html', context)


#view function for viewing single product
@never_cache
def single_product_view(request, pk):
    product_variant = Product_Variant.objects.get(id=pk)
    all_variants = Product_Variant.objects.filter(product_name = product_variant.product_name)
    in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),variant=product_variant).exists() #checking if the item is already added to the cart   
    in_wishlist=False
    if request.user.is_authenticated:
        in_wishlist=Wishlist.objects.filter(user=request.user, product_variant=product_variant).exists()

    context = {
        'product_variant': product_variant,
        'all_variants': all_variants,
        'in_cart'   : in_cart,
        'in_wishlist':in_wishlist,
    }
    return render(request, 'user_home/single_product.html', context)


# view function for searching products through search bar
@never_cache
def search_products_view(request):
    keyword = request.GET.get('keyword', '')
    pet_type_filter = request.GET.getlist('pet_type')
    category_filter = request.GET.getlist('category')
    sort_by = request.GET.get('sort_by', '')

    products = Product_Variant.objects.filter(is_active=True)

    if keyword:
        products = products.filter(
            Q(product_name__description__icontains=keyword) |
            Q(product_name__name__icontains=keyword)
        )

    if pet_type_filter:
        products = products.filter(product_name__pet_type__id__in=pet_type_filter)

    if category_filter:
        products = products.filter(product_name__category__id__in=category_filter)

    # Sorting logic
    if sort_by == 'price_low_high':
        products = products.order_by('price')
    elif sort_by == 'price_high_low':
        products = products.order_by('-price')
    # elif sort_by == 'average_rating':
    #     products = products.order_by('-average_rating')
    # elif sort_by == 'new_arrivals':
    #     products = products.order_by('-created_at')
    elif sort_by == 'az':
        products = products.order_by('product_name__name')
    elif sort_by == 'za':
        products = products.order_by('-product_name__name')
    # elif sort_by == 'popularity':
    #     products = products.order_by('-popularity')
    # elif sort_by == 'featured':
    #     products = products.filter(is_featured=True)

    context = {
        'products': products,
        'count': products.count(),
        'keyword': keyword,
        'pet_types': PetType.objects.filter(is_active=True),
        'categories': Category.objects.filter(is_active=True),
        'selected_pet_types': pet_type_filter,
        'selected_categories': category_filter,
        'sort_by': sort_by,  
    }

    return render(request, 'user_home/search_products.html', context)
