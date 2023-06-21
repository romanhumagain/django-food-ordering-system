from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from Food.models import *
# from django.contrib.auth.models import AbstractUser
# from . manager import UserManager
import django.utils.timezone

# ''# Create your models here.
# class User(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=15, unique=True)

#     objects = UserManager()
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.IntegerField()
    address = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name

class Order(models.Model):
    order_item = models.CharField(max_length=100)
    order_date = models.DateField(default=django.utils.timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    recipe = models.ForeignKey(Recipe , on_delete=models.CASCADE , null=True)
    order_quantity = models.IntegerField()
    order_status = models.CharField(max_length=100, default="Requested")
    total_price = models.IntegerField()
    address = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.order_item
