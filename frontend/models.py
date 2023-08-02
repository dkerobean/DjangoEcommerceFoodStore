
from django.contrib.auth.models import User
from django.db import models
import uuid 
from .utils import generate_order_id
from django.core.validators import MaxValueValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email = models.EmailField(blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='address')
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
    picture = models.ImageField(
        upload_to='category_pictures/', blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
    

class Tag(models.Model):
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
    tag = models.ManyToManyField(Tag)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name 
    

class Review(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_reviews')
    review_text = models.TextField()
    review_title = models.CharField(max_length=50, blank=True, null=True)
    rating = models.PositiveIntegerField(default=5, validators=[MaxValueValidator(5)])
    review_date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user_profile.user.username}"
    
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
