
from django.contrib.auth.models import User
from django.db import models
import uuid 
from .utils import generate_order_id


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email = models.EmailField(blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='addresses')
    country = models.CharField(max_length=100)
    address = models.TextField()
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.address
    
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    product_picture = models.ImageField(
        upload_to='product_pictures/', blank=True, null=True)
    category = models.ManyToManyField(Category)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name 


class Order(models.Model):
    
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product)
    order_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=4, unique=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='PENDING')
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return f"Order #{self.order_id}"
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_order_id()
        super().save(*args, **kwargs)
