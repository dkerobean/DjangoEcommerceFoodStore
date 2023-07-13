from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="admin-login")
def admin_dashboard(request):
    
    return render(request, 'admin_dashboard/index.html')


def admin_login(request):
    
    user = request.user 
    
    # ceck if user is already authenticated 
    if user.is_authenticated and user.is_staff:
        return redirect('admin-dashboard')
    elif request.user.is_authenticated:
        return redirect('index')
    
    
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except UserDoesNotExist:
            messages.error(request,"Invalid Username or Password")
            
        user = authenticate(request, username=username, password=password)
            
        # check for valid credentials
        if user is not None:
            if user.is_staff:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('admin-dashboard')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Username or Password Incorrect')
            return redirect('admin-login')
            
            
    return render(request, 'admin_dashboard/auth/login.html')


def admin_logout(request):
    
    auth_logout(request)
    messages.success(request, 'Logged Out')
    return redirect('admin-login')
