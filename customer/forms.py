from django import forms
from .models import Customer
from django.core.exceptions import ValidationError

class CustomerSignupForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['emailId', 'password', 'name', 'street', 'description', 'pincode', 'city']
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) <= 5:
            raise ValidationError('Password must be more than 5 characters.')
        return password
