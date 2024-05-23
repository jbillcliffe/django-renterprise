from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Submit, Row
from crispy_bootstrap5.bootstrap5 import FloatingField
from localflavor.gb.forms import GBCountySelect
from .models import Customer

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['first_name','last_name','address_line_one',
                'address_line_two','address_line_three',
                'address_line_town', 'address_line_county','postcode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.label_class = 'form-float-label'
        self.helper.layout = Layout(
            Fieldset(
                "Add a new customer :",
                Row(FloatingField('first_name',
                    wrapper_class='col-md-4 mb-3 p-0'),
                    FloatingField('last_name',
                    wrapper_class='col-md-4 mb-3 p-0')),
                Row(FloatingField('address_line_one',
                    wrapper_class='col-md-8 mb-0 p-0')),
                Row(FloatingField('address_line_two',
                    wrapper_class='col-md-8 mb-0 p-0')),
                Row(FloatingField('address_line_three',
                    wrapper_class='col-md-8 mb-3 p-0')),
                Row(FloatingField('address_line_town',
                    wrapper_class='col-md-3 p-0'),
                    FloatingField('address_line_county',
                    wrapper_class='col-md-3 p-0'),
                    FloatingField('postcode',
                    wrapper_class='col-md-2 p-0'))
            ),
            Submit('submit', 'Submit',
                wrapper_class='button centre-align'),
        )

        
