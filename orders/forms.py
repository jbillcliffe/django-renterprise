from django import forms
from django.db.models import CharField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Submit, Row, Field
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import Order
from items.models import Item, ItemType


# https://stackoverflow.com/questions/73789407/django-summernote-clean-got-an-unexpected-keyword-argument-styles-in-djangof
class OrderForm(forms.ModelForm):
    #queryset = ItemType.objects.values_list('category', flat=True).order_by("category")
    queryset= ItemType.objects.values_list("category", flat=True).order_by("category").distinct("category")
    item_type_field = forms.ModelChoiceField(queryset)
    #item = forms.ModelChoiceField(queryset=Item.objects.all())

    class Meta:
        model = Order
        fields = ['item_type_field', 'item', 'cost_initial', 'cost_week',
                'start_date', 'end_date', ]
        widgets = {     
            'start_date': forms.TextInput(attrs={'type': 'date'}),
            'end_date': forms.TextInput(attrs={'type': 'date'}),
        }


    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.label_class = 'form-float-label'
        self.helper.layout = Layout(
            Fieldset(
                "Add a new order :",
                Row(FloatingField('start_date',
                    wrapper_class='col-md-4 mb-0 p-0'),
                    FloatingField('end_date',
                    wrapper_class='col-md-4 mb-0 p-0')),
                Row(FloatingField('item',
                    wrapper_class='col-md-8 mb-3 p-0')),
                Row(FloatingField('cost_initial',
                    wrapper_class='col-md-4 mb-0 p-0'),
                    FloatingField('cost_week',
                    wrapper_class='col-md-4 mb-0 p-0'))
                
            ),
            Submit('submit', 'Submit',
                wrapper_class='button centre-align'),
        )
    """
