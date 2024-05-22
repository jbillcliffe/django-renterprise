from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from localflavor.gb.forms import GBCountySelect

class CustomerForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    address_line_1 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'First Line of Address'})
    )
    address_line_2 = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': 'Line 2'}))
    address_line_3 = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': 'Line 3'}))
    address_line_town = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Town'}))
    address_line_county = GBCountySelect()
    postcode = forms.CharField(label='Postcode')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'address_line_1',
            'address_line_2',
            'address_line_3',
            Row(
                Column('town', css_class='form-group col-md-4'),
                Column('county', css_class='form-group col-md-5'),
                Column('postcode', css_class='form-group col-md-3'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit')
        )