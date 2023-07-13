from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index_page, name="index"), 
    path('shop/', views.shop_page, name="shop"), 
    path('about/', views.about_page, name="about"), 
    path('contact/', views.contact_page, name="contact"),
    path('account/', views.account_dashboard, name="user-dashboard"),
    
    path('login/', views.user_login, name="user-login"),
    path('register/', views.user_register, name="register"),
    path('logout/', views.user_logout, name="user-logout"),
    
    path('activate/<str:uidb64>/<str:token>/', views.activate_user_account, name='activate'),
]
