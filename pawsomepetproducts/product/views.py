from django.shortcuts import render,redirect
from .models import Product_Variant
from .models import Product
from .forms import AddProductForm,AddProductVariantForm
# Create your views here.
#-------------------------admin side views----------------------------------

#view function for listing the products
def admin_products_view(request):
    query=request.GET.get('q')
    if query:
        products=Product.objects.filter(name__icontains=query)
    else:
        products=Product.objects.all()
    return render(request, 'admin/admin_products.html', {'products': products})

#view fucntion for editing the product 
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
def admin_product_variants_view(request):
    query=request.GET.get('q')
    if query:
        product_variants=Product_Variant.objects.filter(name__icontains=query)
    else:
        product_variants=Product_Variant.objects.all()
    return render(request, 'admin/admin_product_variants.html', {'product_variants': product_variants})

#view fucntion for editing the product variant 
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
def admin_add_product_variant_view(request):
    if request.method == 'POST':        
        form=AddProductVariantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_product_variants')
    else:
        form=AddProductVariantForm()
    return render(request, 'admin/admin_add_product_variant.html', {'form':form})


#-------------------------user side views----------------------------------

#view function for all products page
def all_products_view(request):
    products = Product_Variant.objects.all()
    return render(request, 'user_home/all_products.html', {'products': products})


#view function for viewing single product

def single_product_view(request, pk):
    product = Product_Variant.objects.get(id=pk)
    return render(request, 'user_home/single_product.html', {'product': product})