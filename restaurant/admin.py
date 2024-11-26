from django.contrib import admin
from .models import Restaurant, MenuItem

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'emailId', 'city', 'created')
    search_fields = ['name', 'emailId']
    
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'restaurant', 'created')
    search_fields = ['name', 'restaurant__name']
