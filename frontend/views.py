from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from .forms import UserRegistrationForm

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
import base64
from .models import Category, Product, Tag, Review

from .tokens import account_activation_token
import random
from django.db.models import Avg





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

    return render(request, 'frontend/ui/index.html')\
                    


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
            return redirect('index')
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


def account_dashboard(request):
    
    #user = Profile.objects.get(id=pk)
    
    return render(request, 'frontend/ui/account.html')


def shop_page(request):

    return render(request, 'frontend/ui/shop.html')


def about_page(request):

    return render(request, 'frontend/ui/about.html')


def contact_page(request):

    return render(request, 'frontend/ui/contact.html')
