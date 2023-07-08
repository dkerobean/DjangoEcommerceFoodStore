from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegisterationForm


""" AUTH """

def user_login(request):
    
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except UserNotFound:
            messages.error(request,"Username or Password is incorrect")
            return redirect('index')
            
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            messages.error(request, 'Username or Passwors incorrect')
            return redirect('shop')
        
        login(request, user)
        messages.success(request, 'Logged in')
        return redirect('contact')
        
         
    return render(request, 'frontend/ui/index.html')


def get_user_registration_form():
    return UserRegisterationForm()


def user_register(request):
    
    form = get_user_registration_form()
    
    if request.method == "POST":
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successfull')
            return redirect('index')
        else:
            messages.error(request, 'Something went wrong')
        
    context = {
        'form':form
    }
    
    return render(request, 'frontend/ui/index.html', context)



def index_page(request):
    
    form = get_user_registration_form()
    
    context = {
        'form':form
    }
    
    return render(request, 'frontend/ui/index.html', context)


def shop_page(request):

    return render(request, 'frontend/ui/shop.html')


def about_page(request):

    return render(request, 'frontend/ui/about.html')


def contact_page(request):

    return render(request, 'frontend/ui/contact.html')
