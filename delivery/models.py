from django.db import models

class Delivery(models.Model):
    emailId = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
