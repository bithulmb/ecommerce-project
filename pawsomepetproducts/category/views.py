from django.shortcuts import render,redirect
from .models import Category
from .forms import AddCategoryForm
from django.contrib import messages



# Create your views here.


#view function for listing categories and searching in category manangement page
def admin_category_view(request):
    if not (request.user.is_authenticated and request.user.is_superadmin):
        messages.error(request,"You have not logged in. Please login to continue")
        return redirect('admin_login')
    query=request.GET.get('q')
    if query:
        categories=Category.objects.filter(name__icontains=query)
    else:
        categories=Category.objects.all()
    return render(request, 'admin/admin_category.html', {'categories': categories})

#view function for adding new category
def admin_add_category_view(request):
    if not (request.user.is_authenticated and request.user.is_superadmin):
        messages.error(request,"You have not logged in. Please login to continue")
        return redirect('admin_login')
    if request.method == 'POST':        
        form=AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_category')
    else:
        form=AddCategoryForm()
    return render(request, 'admin/admin_add_category.html', {'form':form})


#view function for editing category
def admin_edit_category_view(request,pk):
    if not (request.user.is_authenticated and request.user.is_superadmin):
        messages.error(request,"You have not logged in. Please login to continue")
        return redirect('admin_login')
    object=Category.objects.get(id=pk)
    if request.method == 'POST':
        form=AddCategoryForm(request.POST, instance = object)
        if form.is_valid():
            form.save()
            return redirect('admin_category')
    else:
        form=AddCategoryForm(instance = object)
    return render(request, 'admin/admin_edit_category.html', {'form':form})