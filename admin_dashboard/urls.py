from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.admin_dashboard, name="admin-dashboard" ),
    
    path('login/', views.admin_login, name="admin-login"),
    path('logout/', views.admin_logout, name="admin-logout"),
    
    path('add_category/', views.add_category, name="add-category"),
    path('delete_category/<str:pk>/', views.delete_category, name="delete-category"),
]
