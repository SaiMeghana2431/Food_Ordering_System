from django import forms
from .models import Delivery

class DeliverySignupForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['emailId', 'password', 'name', 'city']
        widgets = {
            'password': forms.PasswordInput(),
        }
