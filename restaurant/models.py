import uuid
from django.db import models

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emailId = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    street = models.TextField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    pincode = models.IntegerField()
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='restaurant_photos/', null=True, blank=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="menu_items", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)  
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
