from django import forms

class RoleSelectionForm(forms.Form):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('delivery', 'Delivery'),
        ('restaurant', 'Restaurant'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
