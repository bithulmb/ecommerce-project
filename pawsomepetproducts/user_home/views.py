from django.shortcuts import render, redirect
from accounts.forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def home_view(request):
    return render(request,'user_home/home.html')


def login_view(request):

     #if already loggedin redirect to home
    if request.user.is_authenticated:
        return redirect('home_page')
        
    #Getting the details for signing in
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        user=authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('home_page')
        else:
            messages.error(request,"Invalid Credentials. Try Again")
            return redirect('login_page')
    return render(request,'user_home/login.html')


def signup_view(request):

    #if request is get render the registration form
    if request.method == 'GET':
        form = RegisterForm()
        return render(request,'user_home/signup.html', {'form':form})
    
    #if requet is POST check for form validation and save the details
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.succes(request, "User created Succesfully. Please login")
            return redirect('login_page')
        else:
            return render(request,'user_home/signup.html',{'form': form})

def all_products_view(request):
    return render(request, 'user_home/all_products.html')

def about_us_view(request):
    return render(request, 'user_home/about_us.html')


def contact_us_view(request):
    return render(request, 'user_home/contact_us.html')
        
        
