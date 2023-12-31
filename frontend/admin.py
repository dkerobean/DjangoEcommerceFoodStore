from django.contrib import admin
from .models import UserProfile, Category, Product, Order, \
  Address, Review, Cart, CartItem

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
