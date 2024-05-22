from .models import Customer
from django import forms

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'address_line_one',
            'address_line_two', 'address_line_three', 'address_line_town',
            'address_line_county', 'postcode')