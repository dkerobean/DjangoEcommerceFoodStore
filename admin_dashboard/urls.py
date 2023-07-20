from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.admin_dashboard, name="admin-dashboard" ),
    
    path('login/', views.admin_login, name="admin-login"),
    path('logout/', views.admin_logout, name="admin-logout"),
    
    path('add_category/', views.add_category, name="add-category"),
    path('delete_category/<str:pk>/', views.delete_category, name="delete-category"),
    
    path('add_product/', views.add_product, name="add-product"),
    path('view_products/', views.view_products, name="view-products"),
    path('product_details/<str:pk>/', views.product_detail, name="product-details"), 
    path('edit_product/<str:pk>/', views.edit_product, name="edit-product"),
    
    path('add_tag/', views.create_tag, name="create-tag"), 
    path('delete_tag/<str:pk/', views.delete_tag, name="delete-tag"),
]
