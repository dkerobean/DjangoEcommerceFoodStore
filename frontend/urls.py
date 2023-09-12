from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name="index"),
    path('shop/', views.shop_page, name="shop"),
    path('about/', views.about_page, name="about"),
    path('contact/', views.contact_page, name="contact"),
    path('account/', views.account_dashboard, name="user-dashboard"),

    path('view_product/<str:pk>/', views.view_product, name="view-product"),
    path('products/<str:q>/', views.filter_products, name="filter-product"),

    path('add_to_cart/<str:product_id>/', views.add_to_cart, name="add-to-cart"),  # noqa
    path('remove_from_cart/<str:cart_item_id>/', views.remove_from_cart, name="remove-from-cart"),  # noqa
    path('cart/', views.view_cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('order_complete', views.order_complete, name="order-complete"),
    path('delete_order/<str:order_id>/', views.delete_order, name="delete-order"),   # noqa

    path('login/', views.user_login, name="user-login"),
    path('register/', views.user_register, name="register"),
    path('logout/', views.user_logout, name="user-logout"),
    path('auth/', views.login_register, name="login-register"),

    path('activate/<str:uidb64>/<str:token>/', views.activate_user_account, name='activate'),   # noqa
]
