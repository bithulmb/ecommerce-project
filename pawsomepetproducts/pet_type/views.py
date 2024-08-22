from django.shortcuts import render,redirect
from .models import PetType
from .forms import AddPetTypeForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from accounts.decorators import superuser_required
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator


# Create your views here.

#view function for the listing of the pet types and searching pet types
@superuser_required
@never_cache
def admin_pet_type_view(request):
    query=request.GET.get('q')
    if query:
        pet_types=PetType.objects.filter(name__icontains=query)
    else:
        pet_types=PetType.objects.all()
    
    #for pagination
    paginator = Paginator(pet_types, 8) 
    page = request.GET.get('page')
    try:
        pet_types = paginator.page(page)
    except PageNotAnInteger:
        pet_types = paginator.page(1)
    except EmptyPage:
        pet_types = paginator.page(paginator.num_pages)

        
    return render(request, 'admin/admin_pet_type.html', {'pet_types': pet_types})


#view function for adding pet type
@superuser_required
@never_cache
def admin_add_pet_type_view(request):
    if request.method == 'POST':        
        form=AddPetTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Pet Type added succesfully")
            return redirect('admin_pet_type')
    else:
        form=AddPetTypeForm()
    return render(request, 'admin/admin_add_pet_type.html', {'form':form})


#view function for editing the pet types.
@superuser_required
@never_cache
def admin_edit_pet_type_view(request,pk):
    object=PetType.objects.get(id=pk)
    if request.method == 'POST':
        form=AddPetTypeForm(request.POST, instance = object)
        if form.is_valid():
            form.save()
            messages.success(request,"Pet Type details updated succesfully")
            return redirect('admin_pet_type')
    else:
        form=AddPetTypeForm(instance = object)
    return render(request, 'admin/admin_edit_pet_type.html', {'form':form})