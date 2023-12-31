from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.admin_dashboard, name="admin-dashboard"),

    path('login/', views.admin_login, name="admin-login"),
    path('logout/', views.admin_logout, name="admin-logout"),

    path('add_category/', views.add_category, name="add-category"),
    path('delete_category/<str:pk>/', views.delete_category, name="delete-category"), # noqa
    path('edit_category/<str:pk>/', views.edit_category, name="edit-category"), # noqa

    path('add_product/', views.add_product, name="add-product"),
    path('view_products/', views.view_products, name="view-products"),
    path('product_details/<str:pk>/', views.product_detail, name="product-details"), # noqa
    path('edit_product/<str:pk>/', views.edit_product, name="edit-product"),
    path('delete_product/<str:pk>/', views.delete_product, name="delete-product"), # noqa

    path('add_tag/', views.create_tag, name="create-tag"),
    path('delete_tag/<str:pk>/', views.delete_tag, name="delete-tag"),

    path('all_users/', views.list_users, name="list-users"),
    path('deactivate_user/<str:pk>/', views.deactivate_user, name="deactivate-user"), # noqa

    path('view_reviews/', views.user_review, name="view-reviews"),
    path('delete_review/<str:pk>/', views.delete_review, name="delete-review"),

    path('order_history', views.order_history, name="order-history"),
]
