from django import forms
from .models import Restaurant, MenuItem

class RestaurantSignupForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['emailId', 'password', 'name', 'street', 'description', 'pincode', 'city','image']
        widgets = {
            'password': forms.PasswordInput(),
        }
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'image']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add 'form-control' class to each form field
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})