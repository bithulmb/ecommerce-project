from django.shortcuts import render,redirect
from .models import Category
from .forms import AddCategoryForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from accounts.decorators import superuser_required
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.


#view function for listing categories and searching in category manangement page
@superuser_required
@never_cache
def admin_category_view(request):
    query=request.GET.get('q')
    if query:
        categories=Category.objects.filter(name__icontains=query)
    else:
        categories=Category.objects.all().order_by('-id')

    #for pagination
    paginator = Paginator(categories, 8) 
    page = request.GET.get('page')
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    
    return render(request, 'admin/admin_category.html', {'categories': categories})

#view function for adding new category
@superuser_required
@never_cache
def admin_add_category_view(request):
    if request.method == 'POST':        
        form=AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Category added succesfully")
            return redirect('admin_category')
    else:
        form=AddCategoryForm()
    return render(request, 'admin/admin_add_category.html', {'form':form})


#view function for editing category
@superuser_required
@never_cache
def admin_edit_category_view(request,pk):
    object=Category.objects.get(id=pk)
    if request.method == 'POST':
        form=AddCategoryForm(request.POST, instance = object)
        if form.is_valid():
            form.save()
            messages.success(request,"Category details updated succesfully")
            return redirect('admin_category')
    else:
        form=AddCategoryForm(instance = object)
    return render(request, 'admin/admin_edit_category.html', {'form':form})