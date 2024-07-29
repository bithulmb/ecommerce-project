from django.shortcuts import render,redirect
from .models import Category
from .forms import AddCategoryForm



# Create your views here.


#view for displaying category manangement page
def admin_category_view(request):
    categories=Category.objects.all()
    return render(request, 'admin/admin_category.html', {'categories': categories})


def admin_add_category_view(request):
    if request.method == 'POST':        
        form=AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_category')
    else:
        form=AddCategoryForm()
    return render(request, 'admin/admin_add_category.html', {'form':form})



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