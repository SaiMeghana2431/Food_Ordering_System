from django import forms
from .models import Delivery
from django.core.exceptions import ValidationError

class DeliverySignupForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['emailId', 'password', 'name', 'city']
        widgets = {
            'password': forms.PasswordInput(),
        }
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) <= 3:
            raise ValidationError('Password must be more than 5 characters.')
        return password