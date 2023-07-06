from django.contrib import admin
from .models import UserProfile, Category, Product, Order

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
