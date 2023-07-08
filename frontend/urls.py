from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index_page, name="index"), 
    path('shop/', views.shop_page, name="shop"), 
    path('about/', views.about_page, name="about"), 
    path('contact/', views.contact_page, name="contact"), 
    
    path('login/', views.user_login, name="login"),
    path('register/', views.user_register, name="register")
]
