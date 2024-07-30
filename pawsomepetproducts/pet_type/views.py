from django.shortcuts import render,redirect
from .models import PetType
from .forms import AddPetTypeForm

# Create your views here.

#view function for the listing of the pet types and searching pet types
def admin_pet_type_view(request):
    query=request.GET.get('q')
    if query:
        pet_types=PetType.objects.filter(name__icontains=query)
    else:
        pet_types=PetType.objects.all()
    return render(request, 'admin/admin_pet_type.html', {'pet_types': pet_types})


#view function for adding pet type
def admin_add_pet_type_view(request):
    if request.method == 'POST':        
        form=AddPetTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_pet_type')
    else:
        form=AddPetTypeForm()
    return render(request, 'admin/admin_add_pet_type.html', {'form':form})


#view function for editing the pet types.
def admin_edit_pet_type_view(request,pk):
    object=PetType.objects.get(id=pk)
    if request.method == 'POST':
        form=AddPetTypeForm(request.POST, instance = object)
        if form.is_valid():
            form.save()
            return redirect('admin_pet_type')
    else:
        form=AddPetTypeForm(instance = object)
    return render(request, 'admin/admin_edit_pet_type.html', {'form':form})