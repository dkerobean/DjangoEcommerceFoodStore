from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from frontend.models import Category, Product, Tag
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .forms import AddProductForm

# check if user is Admin
def is_staff(user):
    return user.is_staff and user.is_authenticated
    
    
@user_passes_test(is_staff)
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

@user_passes_test(is_staff)
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


@user_passes_test(is_staff)
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


""" PRODUCT """

@user_passes_test(is_staff)
def add_product(request):
    
    form = AddProductForm()
    
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Added")
            return redirect('add-product')
        else:
            messages.error(request, 'Something went wrong')
            return redirect('add-product')
        
    context = {
        'form': form
    }
                
    
    return render(request, 'admin_dashboard/product/add_product.html', context)


@user_passes_test(is_staff)
def view_products(request):
    
    products = Product.objects.all()
    
    context = {
        'products' : products
    }
    
    
    return render(request, 'admin_dashboard/product/view_products.html', context)


@login_required(login_url="admin-login")
@user_passes_test(is_staff)
def product_detail(request, pk):
    
    product = Product.objects.get(id=pk)
    
    context = {
        'product' : product
    }
    
    return render(request, 'admin_dashboard/product/product_details.html', context)


@user_passes_test(is_staff)
def edit_product(request, pk):
    
    product = Product.objects.get(id=pk)
    
    form = AddProductForm(instance=product)
    
    if request.method == "POST":
        form = AddProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Prduct Edited Succesfully')
            return redirect('view-products')
        else:
            messages.error(request, 'Something went wrong')
            return redirect('view-products')
        
    context = {
        'form':form
    }
            
    
    return render(request, 'admin_dashboard/product/add_product.html', context)


""" TAGS """

@user_passes_test(is_staff)
def create_tag(request):
    
    if request.method == "POST":
        tagname = request.POST['tagName']
        
        if not tagname:
            messages.error(request, 'Please enter a tag name')
            
        tag = Tag.objects.create(name=tagname)
        tag.save()
        messages.success(request, "Tag created")
        return redirect('create-tag')
        
    tags = Tag.objects.all()
    
    conntext = {
        'tags' : tags
    }
        
        
    return render(request, 'admin_dashboard/tag/add_tag.html', conntext)


@user_passes_test(is_staff)
def delete_tag(request, id):
    
    tag = Tag.objects.get(id=pk)
    
    try:
        tag.delete()
        messages.success(request, 'Tag deleted')
        return redirect('create-tag')
    except TagNotFound:
        messages.error(request, 'Tag not found')
    
    return render(request, 'admin_dashboard/tag/add_tag.html')


""" USER LIST """

def list_users(request):
    
    all_users = User.objects.all()
    
    
    context = {
        'all_users': all_users
    }
    
    
    return render(request, 'admin_dashboard/users/list_users.html', context)
    
    
    
    
    
    
    
