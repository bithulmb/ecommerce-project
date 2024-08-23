from django.shortcuts import render,redirect,get_object_or_404
from .models import Product_Variant,Product_Images,ReviewRating
from .models import Product
from pet_type.models import PetType
from category.models import Category
from .forms import AddProductForm,AddProductVariantForm,AddProductImages,ReviewForm
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
from accounts.decorators import superuser_required
from django.contrib.auth.decorators import login_required
from orders.models import OrderProduct
from django.db.models import Avg



# Create your views here.
#-------------------------admin side views----------------------------------

#view function for listing the products
@superuser_required
@never_cache
def admin_products_view(request):
    query=request.GET.get('q')
    if query:
        products=Product.objects.filter(name__icontains=query)
    else:
        products=Product.objects.all().order_by('-id')
    
    #for pagination
    paginator = Paginator(products, 8) 
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)


    return render(request, 'admin/admin_products.html', {'products': products})

#view fucntion for editing the product 
@superuser_required
@never_cache
def admin_edit_product_view(request,pk):
    object=Product.objects.get(id=pk)
    if request.method == 'POST':
        form=AddProductForm(request.POST, instance = object)
        if form.is_valid():
            form.save()
            messages.success(request," Product details updated succesfully")
            return redirect('admin_products')
    else:
        form=AddProductForm(instance = object)
    return render(request, 'admin/admin_edit_product.html', {'form':form})

#view function for adding new product
@superuser_required
@never_cache
def admin_add_product_view(request):
    if request.method == 'POST':        
        form=AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added succesfully")
            return redirect('admin_products')
    else:
        form=AddProductForm()
    return render(request, 'admin/admin_add_product.html', {'form':form})


#view fucntion for listing product variants
@superuser_required
@never_cache
def admin_product_variants_view(request):
    query=request.GET.get('q')
    if query:
        product_variants=Product_Variant.objects.filter(name__icontains=query)
    else:
        product_variants=Product_Variant.objects.all().order_by('-id')

    #for pagination
    paginator = Paginator(product_variants, 8) 
    page = request.GET.get('page')
    try:
        product_variants = paginator.page(page)
    except PageNotAnInteger:
        product_variants = paginator.page(1)
    except EmptyPage:
        product_variants = paginator.page(paginator.num_pages)
    return render(request, 'admin/admin_product_variants.html', {'product_variants': product_variants})

#view fucntion for editing the product variant 
@superuser_required
@never_cache
def admin_edit_product_variant_view(request,pk):
    object=Product_Variant.objects.get(id=pk)
    if request.method == 'POST':
        form=AddProductVariantForm(request.POST, instance = object)
        if form.is_valid():
            form.save()
            messages.success(request,"Product Variant details updated succesfully")
            return redirect('admin_product_variants')
    else:
        form=AddProductVariantForm(instance = object)
    return render(request, 'admin/admin_edit_product_variant.html', {'form':form})


#view function for adding new product variant
@superuser_required
@never_cache
def admin_add_product_variant_view(request):
    if request.method == 'POST':        
        form=AddProductVariantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Product Variant added succesfully")
            return redirect('admin_product_variants')
    else:
        form=AddProductVariantForm()
    return render(request, 'admin/admin_add_product_variant.html', {'form':form})

#view for adding images and editing images for product variants
@superuser_required
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
    page = request.GET.get('page', 1)

    products = Product_Variant.objects.filter(is_active=True).order_by('-id')

    if pet_type_ids:
        products = products.filter(product_name__pet_type__id__in=pet_type_ids)
    if category_ids:
        products = products.filter(product_name__category__id__in=category_ids)

    if sort_by == 'price_low_high':        
        products = products.order_by('price')
    elif sort_by == 'price_high_low':
        products = products.order_by('-price')
    elif sort_by == 'az':
        products = products.order_by('product_name__name')
    elif sort_by == 'za':
        products = products.order_by('-product_name__name')
    elif sort_by == 'average_rating':
        products = products.order_by('-average_rating')
    elif sort_by == 'featured':
        products = products.order_by('-is_featured')
       

    paginator = Paginator(products, 9)
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'pet_types': PetType.objects.filter(is_active=True),
        'categories': Category.objects.filter(is_active=True),
        'count': products.count(),
        'selected_pet_types': pet_type_ids,
        'selected_categories': category_ids, 
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            template_name="user_home/product_list_partial.html", 
            context=context
        )
        data = {
            "html": html,
            "has_next": paged_products.has_next(),
            "has_previous": paged_products.has_previous(),
            "page": paged_products.number,
            "total_pages": paginator.num_pages,
            "count": products.count()
        }
        return JsonResponse(data)

    return render(request, 'user_home/all_products.html', context)



#view function for viewing single product
@never_cache
def single_product_view(request, pk):
    product_variant = Product_Variant.objects.get(id=pk)
    all_variants = Product_Variant.objects.filter(product_name = product_variant.product_name)
    in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),variant=product_variant).exists() #checking if the item is already added to the cart   
    
    #checking if the item is in wishlist for displaying wishlist button
    in_wishlist=False
    if request.user.is_authenticated:
        in_wishlist=Wishlist.objects.filter(user=request.user, product_variant=product_variant).exists()
    
    #checking if the product is ordered by user to display the review form
    try:        
        product_ordered=OrderProduct.objects.filter(order__user=request.user, product = product_variant).exists()
        
    except:
        product_ordered=False

    #getting the reviews related to the product
    reviews=ReviewRating.objects.filter(product_variant=product_variant, status=True)

    context = {
        'product_variant': product_variant,
        'all_variants': all_variants,
        'in_cart'   : in_cart,
        'in_wishlist':in_wishlist,
        'product_ordered' : product_ordered,
        'reviews'   :reviews
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


#view for submitting reviews
@login_required(login_url='login_page')
def submit_review_view(request,variant_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id, product_variant__id = variant_id)
            form    = ReviewForm(request.POST, instance = reviews)
           
            form.save()
            messages.success(request, "Thank You. Your review has been updated")
            
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form    = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.product_variant_id = variant_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank You. Your review has been submitted")
                return redirect(url)

