from django import forms
from django.db.models import CharField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, HTML

from crispy_bootstrap5.bootstrap5 import FloatingField

from localflavor.gb.forms import GBCountySelect

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextField
from .admin import CustomerNoteAdmin
from .models import Customer, CustomerNote

# https://stackoverflow.com/questions/73789407/django-summernote-clean-got-an-unexpected-keyword-argument-styles-in-djangof
class CustomerForm(forms.ModelForm):

    #address_line_county = GBCountySelect()
    
    class Meta:
        model = Customer
        fields = ['first_name','last_name','address_line_one',
                'address_line_two','address_line_three',
                'address_line_town', 'address_line_county','postcode']

        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "address_line_one": "First Line of Address",
            "address_line_two": "Second Line of Address",
            "address_line_three": "Third Line of Address",
            "address_line_town": "Town",
            "address_line_county": "County",
            "postcode": "Postcode"
        }

    #https://github.com/django-crispy-forms/django-crispy-forms/issues/158
    #Bootstrap kept overriding button style when it is unwanted.
    #Have to use javascript to submit the form and keep FloatingField styles

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'form-float-label'
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.layout = Layout(
            Row(FloatingField('first_name',
            wrapper_class='col-md-4 mb-1 p-0'),
            FloatingField('last_name',
            wrapper_class='col-md-6 mb-1 p-0')),
            Row(FloatingField('address_line_one',
            wrapper_class='col-md-10 mb-1 p-0')),
            Row(FloatingField('address_line_two',
            wrapper_class='col-md-10 mb-1 p-0')),
            Row(FloatingField('address_line_three',
            wrapper_class='col-md-10 mb-1 p-0')),
            Row(FloatingField('address_line_town',
            wrapper_class='col-md-4 mb-1 p-0'),
            FloatingField('address_line_county',
            wrapper_class='col-md-4 mb-1 p-0'),
            FloatingField('postcode',
            wrapper_class='col-md-2 mb-1 p-0')),
            Row(HTML('<input class="button col-md-10" type="submit" name="submit" value="Submit" id="submit-id-submit">'),
                HTML('<a class="button centre-align col-md-10" style="margin-top: 1.5vh; margin-left: 8px;" href="{% url \'customers:customer_list\' %}">Return To Customer List </a>')),
        )


class CustomerNoteForm(forms.ModelForm):
    class Meta:
        model = CustomerNote
        fields = ('note',)
        labels = {
            "note": "Note"
        }