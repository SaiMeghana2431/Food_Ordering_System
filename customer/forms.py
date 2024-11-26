from django import forms
from .models import Customer

class CustomerSignupForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['emailId', 'password', 'name', 'street', 'description', 'pincode', 'city']
        widgets = {
            'password': forms.PasswordInput(),
        }
