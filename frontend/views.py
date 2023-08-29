from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from .forms import UserRegistrationForm, UserProfileEditForm, UserAddressEditForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
import base64
from .models import Category, Product, Tag, Review, Address, Order

from .tokens import account_activation_token
import random
from django.db.models import Avg
from django.contrib.auth.models import AnonymousUser

    

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
            messages.error(request, 'Username or Password incorrect')
            return redirect('login-register')
        
        login(request, user)
        messages.success(request, 'Logged in')
        return redirect('user-dashboard')
        
         
    return render(request, 'frontend/ui/index.html')


def user_logout(request):
    
    auth_logout(request)
    messages.success(request, 'Logged Out')
    return redirect('index')

    return render(request, 'frontend/ui/index.html')
                    


def get_user_registration_form():
    return UserRegistrationForm()


def login_register(request):
    
    form = UserRegistrationForm()
    
    context = {
        "form" : form
    }
    
    return render(request, 'frontend/auth/login_register.html', context)


def user_register(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send Confirmation Email
            current_site = get_current_site(request)
            uidb64 = urlsafe_base64_encode(user.pk.to_bytes(4, 'big'))
            token = account_activation_token.make_token(user)
            activation_link = f"http://{current_site.domain}/activate/{uidb64}/{token}/"

            mail_subject = 'Activate your account'
            message = render_to_string('frontend/auth/confirmation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            send_mail(mail_subject, message,
                      'accounts@panda.com', [user.email])

            messages.success(
                request, 'Registration successful. Please check your email to activate your account.')
            return redirect('admin-dashboard')
        else:
            messages.error(request, 'Something went wrong')

    context = {
        'form': form
    }

    return render(request, 'frontend/ui/index.html', context)



def activate_user_account(request, uidb64, token):
    try:
        #uid = urlsafe_base64_decode(uidb64)
        uid = urlsafe_base64_decode(uidb64)
        print(f"UIDB {uid}")
        user_id = int_value = int.from_bytes(uid, byteorder='big')
        print(f"user id {user_id}")
        user = get_user_model().objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        messages.error(request, 'User not found')

    if user is not None and account_activation_token.check_token(user, token):
        # Activate user account
        user.is_active = True
        user.save()
        messages.success(request, 'Email Verified')
        return redirect('index')
    else:
        messages.error(request, 'Token is invalid ')
        return redirect('index')


        
def index_page(request):
    
    form = get_user_registration_form()
    categories = Category.objects.all()

    top_products = Product.objects.filter(tag__name="top")
    new_arrivals = Product.objects.filter(tag__name="New arrivals")
    featured_products = Product.objects.filter(tag__name="featured")

    
    context = {
        'form':form, 
        'categories':categories,
        'top_products':top_products,
        'new_arrivals':new_arrivals, 
        "featured":featured_products 
    }
    
    return render(request, 'frontend/ui/index.html', context)


def view_product(request, pk):
    
    product = Product.objects.get(id=pk)
    product_id = product.id
    
    form = get_user_registration_form()
    
    #get all products excluding current product
    other_products = Product.objects.exclude(id=pk)
    
    # Convert the QuerySet into a list
    other_products_list = list(other_products)

    # Shuffle the list to randomize the order of products
    random.shuffle(other_products_list)
    
    # Limit the number of related products to 4
    related_products = other_products_list[:4]
    
    # product categories 
    categories = product.category.all()
    
    # product tags
    tags = product.tag.all() 
          
    # add review
    if request.method =='POST':    
            
        title = request.POST.get('title')
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        user = request.user
        
        # Check if the user has already submitted a review for this product
        existing_review = Review.objects.filter(
            product_id=product_id, user_profile=user.profile).exists()

        if existing_review:
            messages.error(
                request, 'You have already submitted a review for this product.')
            return redirect('view-product', product_id)
        
        user_review = Review.objects.create(review_text=review, review_title=title,
                                            rating=rating, product=product, user_profile=user.profile)
        user_review.save()
        messages.success(request, 'Product rated')
        return redirect('view-product', product_id)
    
    
    reviews = Review.objects.filter(product=product)
    
    # Calculate the average rating for the product
    avg_rating = reviews.aggregate(average_rating=Avg('rating'))[
        'average_rating']
    

    context = {
        "product":product,
        "related_products" : related_products, 
        "categories":categories,
        "tags":tags,
        "form":form, 
        "reviews":reviews, 
        "average_rating": round(avg_rating, 2) / 20 if avg_rating else 0.0,
        "avg_rating":avg_rating
    }
    
    return render(request, 'frontend/product/view_product.html', context)



""" SHOP """

def shop_page(request):
    
    categories = Category.objects.all()
    products = Product.objects.all()
    tags = Tag.objects.all()
    
    ratings = {}  # Create an empty dictionary to store average ratings for each product

    for product in products:
        # Retrieve the average rating for the product
        average_rating = product.product_reviews.aggregate(Avg('rating'))['rating__avg']
        # Round the average rating to 2 decimal places
        average_rating = round(average_rating, 2) if average_rating else None
        # Store the average rating in the ratings dictionary with the product's ID as the key
        ratings[product.id] = average_rating
        
    
    context = {
        "categories":categories,
        "products":products,  
         "ratings":ratings,
         "tags":tags      
    }    
    

    return render(request, 'frontend/ui/shop.html', context)

def filter_products(request, q):
    
    # get the search query string from the URL
    query = q
    
    products = Product.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if query:
        # filter the products queryset by category using the icontains lookup
        products = products.filter(category__name__icontains=query) | products.filter(tag__name__icontains=query)
        
    context = {
        "products" : products, 
        "categories":categories, 
        "tags":tags
    }
        
    return render(request, 'frontend/ui/shop.html', context)


""" CART PAGES """

@login_required(login_url="login-register")
def add_to_cart(request, product_id):
    
    next_url = request.GET.get('next', 'index')
    
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, product=product)

    # If the product is already in the cart, increase the quantity, else set quantity to 1
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        
    messages.success(request, 'Item added successfully')
    cart_item.save()

    redirect_url = request.META.get('HTTP_REFERER')
    return redirect(redirect_url)


@login_required(login_url="login-register")
def view_cart(request):
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    
    # edit cart quantity
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        product_id = request.POST.get('product_id')
        cart_item = CartItem.objects.get(cart=cart, product=product_id)
        cart_item.quantity = int(quantity)
        cart_item.save()
        messages.success(request, 'Quantity updated successfully')
        return redirect('cart')
            
    context = {
        "cart_items": cart_items, 
    }
    
    return render(request, 'frontend/cart/view_cart.html', context)


@login_required(login_url="login-register")
def remove_from_cart(request, cart_item_id):
    
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    # Decrease the quantity or remove the item from the cart
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        redirect_url = request.META.get('HTTP_REFERER')
        return redirect(redirect_url)
    else:
        cart_item.delete()
        messages.success(request, 'Item removed from cart')
        redirect_url = request.META.get('HTTP_REFERER')
        return redirect(redirect_url)

    return redirect('cart')


@login_required(login_url="login-register")
def checkout(request):
    
    user_profile = request.user.profile
    user_address = Address.objects.get(user_profile=user_profile)
    
    # place order 
    if request.method == 'POST':
        order_total = float(request.POST.get('order_total'))
        
        #get cart items
        cart = Cart.objects.get(user=request.user)
        products = [item.product for item in cart.cartitem_set.all()]
        
        order = Order.objects.create(
            user_profile=user_profile, 
            order_total=order_total
            )
        
        order.products.set(products)
        order.save()
        cart.delete()
        
        messages.success(request, 'Order Placed successfully')
        return redirect('order-complete')
    
    context = {
        'user_address': user_address
    }
    
    return render(request, 'frontend/cart/checkout.html', context)


@login_required(login_url="login-register")
def order_complete(request):
    
    user_profile = request.user.profile
    user_address = Address.objects.get(user_profile=user_profile)
    
    context = {
        'user_address': user_address
    }
    
  
    return render(request, 'frontend/cart/order_complete.html', context)
    

def about_page(request):

    return render(request, 'frontend/ui/about.html')


def contact_page(request):

    return render(request, 'frontend/ui/contact.html')


def account_dashboard(request):
    
    # account info 
    profile_form = UserProfileEditForm()
    user_profile = UserProfile.objects.get(user=request.user)
    
    user = request.user
    user_profile = request.user.profile
    
    #user orders 
    orders = Order.objects.filter(user_profile=request.user.profile)
    
    # user address 
    address_form = UserAddressEditForm()
    
    try:
        user_address = Address.objects.get(user_profile=user_profile)
    except Address.DoesNotExist:
        user_address = None
    
    if request.method == "POST":
        
        # account info
        profile_form = UserProfileEditForm(request.POST, instance=user_profile)
        if profile_form.is_valid():
            user.first_name = profile_form.cleaned_data['first_name']
            user.last_name = profile_form.cleaned_data['last_name']
            user.username = profile_form.cleaned_data['username']
            user.save()
            profile_form.save()
            messages.success(request, 'Addedd Successfully')
            return redirect('user-dashboard')
        
        # user address 
        address_form = UserAddressEditForm(request.POST, instance=user_address)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user_profile = user_profile
            address.save()
            messages.success(request, 'Address Addedd Successfully')
            return redirect('user-dashboard')
                       
    else:
        profile_form = UserProfileEditForm(instance=user_profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        })
        
        address_form = UserAddressEditForm(instance=user_address)
      
        
    context = {
        'profile_form':profile_form,
        'address_form':address_form, 
        'user_address':user_address,
        'orders':orders
    }
    
    
    return render(request, 'frontend/ui/account.html', context)
