from django.shortcuts import render

# Create your views here.

def home_page_view(request):
    return render(request,'home.html')


def login_page_view(request):
    return render(request,'login.html')

def signup_page_view(request):
    return render(request,'signup.html')