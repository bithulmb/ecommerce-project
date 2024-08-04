from django.shortcuts import render,redirect
from .models import CustomUser
from django.db.models import Q
from .forms import RegisterForm,CustomUserUpdateForm,UserProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache

# Create your views here.


#Admin Side views
#-------------------------Admin side views----------------------------------

#view function for listing the users in admin panel
@never_cache
def admin_users_view(request):
    if not (request.user.is_authenticated and request.user.is_superadmin):
        messages.error(request,"You have not logged in. Please login to continue")
        return redirect('admin_login')
    query=request.GET.get('q')
    if query:   #if there is search query
        users=CustomUser.objects.filter(is_superadmin = False).filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query))
    else:
        users=CustomUser.objects.filter(is_superadmin = False)
    return render(request, 'admin/admin_users.html', {'users':users})

@never_cache
def admin_edit_user_view(request, pk):
    if not (request.user.is_authenticated and request.user.is_superadmin):
        messages.error(request,"You have not logged in. Please login to continue")
        return redirect('admin_login')
    object=CustomUser.objects.get(id=pk)
    if request.method == 'POST':
        form=CustomUserUpdateForm(request.POST, instance = object)
        if form.is_valid():
            form.save()
            return redirect('admin_users')
    else:
        form=CustomUserUpdateForm(instance = object)
    return render(request, 'admin/admin_edit_user.html', {'form':form})



# User side views

#-------------------------User side views----------------------------------
@never_cache
def login_view(request):

     #if already loggedin redirect to home
    if request.user.is_authenticated:
        return redirect('home_page')
        
    #Getting the details for signing in
    if request.method=="POST":
        email       = request.POST.get("email")
        password    = request.POST.get("password")
        user        = authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('home_page')
        else:
            messages.error(request,"Invalid Credentials. Try Again")
            return redirect('login_page')
    return render(request,'user_home/login.html')

@never_cache
def signup_view(request):
    #if already loggedin redirect to home
    if request.user.is_authenticated:
        return redirect('home_page')
    
    #if request is get render the registration form
    if request.method == 'GET':
        form = RegisterForm()
        return render(request,'user_home/signup.html', {'form':form})
    
    #if requet is POST check for form validation and save the details
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created Succesfully. Please login")
            return redirect('login_page')
        else:
            return render(request,'user_home/signup.html',{'form': form})

@never_cache
def logout_view(request):
    logout(request)
    return redirect('home_page')
        
        
#view for displaying user profile
def user_profile_view(request):
    object=CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        form=UserProfileForm(request.POST, instance = object)
        if form.is_valid():
            form.save()
            messages.success(request,"User profile Updated succesfully")
            return redirect('user_profile')
    else:
        form=UserProfileForm(instance = object)
    return render(request,'user_home/user_profile.html', {'form':form})
