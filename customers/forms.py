#from .models import Customer
#from django import forms
#
#class CustomerForm(forms.ModelForm):
#    class Meta:
#        model = Customer
#        fields = ('first_name', 'last_name', 'address_line_one',
#            'address_line_two', 'address_line_three', 'address_line_town',
#            'address_line_county', 'postcode')

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class CustomerForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    address_line_1 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'First Line of Address'})
    )
    address_line_2 = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': 'Line 2'}))
    address_line_3 = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': 'Line 3'}))
    address_line_town = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Town'}))
    address_line_county = forms.ChoiceField(choices=STATES)
    zip_code = forms.CharField(label='Zip')
    check_me_out = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'address_1',
            'address_2',
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('zip_code', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            'check_me_out',
            Submit('submit', 'Sign in')
        )