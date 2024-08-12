from django.shortcuts import render,redirect
from .models import Category
from .forms import AddCategoryForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required



# Create your views here.


#view function for listing categories and searching in category manangement page
@staff_member_required(login_url="admin_login")
def admin_category_view(request):
    query=request.GET.get('q')
    if query:
        categories=Category.objects.filter(name__icontains=query)
    else:
        categories=Category.objects.all()
    return render(request, 'admin/admin_category.html', {'categories': categories})

#view function for adding new category
@staff_member_required(login_url="admin_login")
def admin_add_category_view(request):
    if request.method == 'POST':        
        form=AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_category')
    else:
        form=AddCategoryForm()
    return render(request, 'admin/admin_add_category.html', {'form':form})


#view function for editing category
@staff_member_required(login_url="admin_login")
def admin_edit_category_view(request,pk):
    object=Category.objects.get(id=pk)
    if request.method == 'POST':
        form=AddCategoryForm(request.POST, instance = object)
        if form.is_valid():
            form.save()
            return redirect('admin_category')
    else:
        form=AddCategoryForm(instance = object)
    return render(request, 'admin/admin_edit_category.html', {'form':form})