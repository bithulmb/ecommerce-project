from django.shortcuts import render,redirect
from .models import Product_Variant
from .models import Product
from .forms import AddProductForm
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



#-------------------------user side views----------------------------------

def all_products_view(request):
    products=Product_Variant.objects.all()
    return render(request, 'user_home/all_products.html', {'products': products})