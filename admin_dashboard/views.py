from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from frontend.models import Category
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="admin-login")
def admin_dashboard(request):
    
    return render(request, 'admin_dashboard/index.html')


""" AUTH """

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


""" CATEGORY """

def add_category(request):
    
    # add category
    if request.method == "POST":
        name = request.POST["name"]
        image = request.FILES.get("category_image")
        
        # check if fields are provided
        if not name and image:
            messages.error(request, "Pleae provide both name and image")
            return redirect('add-category')
        
        category_object = Category.objects.create(name=name, picture=image)
        category_object.save()
        messages.success(request, "Category created")
        return redirect('add-category')
    
    
    categories = Category.objects.all()
    
    context = {
        'categories':categories
    }
    
       
    return render(request, 'admin_dashboard/category/add_category.html', context)


def delete_category(request, pk):
    
    category_id = Category.objects.get(id=pk)
    
    try:
        category_id.delete()
        messages.success(request, "Deleted Successfully")
        return redirect('add-category')
    except CategoryNotFound:
        messages.error(request, "Category Not Found")
        return redirect('add-category')
    
    return render(request, 'admin_dashboard/category/add_category.html')
    
    
    
    
    
    
