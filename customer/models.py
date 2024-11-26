from django.db import models
from restaurant.models import MenuItem, Restaurant
from django.contrib.auth.models import User
from django.utils.timezone import now

class Customer(models.Model):
    emailId = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    street = models.TextField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    pincode = models.IntegerField()
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.total_price = self.menu_item.price * self.quantity 
        super().save(*args, **kwargs)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    ordered_items = models.JSONField() 
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, default="Pending")
    ordered_at = models.DateTimeField(auto_now_add=True)
    delivery_datetime = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"Order {self.id} from {self.customer.name}"