from django import forms
from django.forms import HiddenInput
from django.db.models import CharField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Submit, Row, Field
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import Order
from items.models import Item, ItemType


# https://stackoverflow.com/questions/73789407/django-summernote-clean-got-an-unexpected-keyword-argument-styles-in-djangof
class OrderForm(forms.ModelForm):
    item_type_categories = ItemType.objects.values_list("category", flat=True).order_by("category").distinct("category")
    item_type_field = forms.ModelChoiceField(item_type_categories, label="Item Category")

    item_type_names = ItemType.objects.values_list("name", flat=True).order_by("name").distinct("name")
    item_type_names_hidden = ItemType.objects.values("name", "category", "cost_initial", "cost_week", "id").order_by("name").distinct("name")

    item_field = forms.ModelChoiceField(item_type_names, label="Item")
    item_field_hidden = forms.ModelChoiceField(item_type_names_hidden)

    full_item_list = Item.objects.values("item_type", "item_serial", "delivery_date",
                                         "collect_date", "repair_date", "status")
    full_item_hidden = forms.ModelChoiceField(full_item_list)

    class Meta:
        model = Order
        fields = ['item_type_field', 'item_field',
                'item_field_hidden', 'full_item_hidden', 'cost_initial',
                'cost_week', 'start_date', 'end_date']
        widgets = {     
            'start_date': forms.TextInput(attrs={'type': 'date'}),
            'end_date': forms.TextInput(attrs={'type': 'date'}),
        }
        labels = {
            "start_date": "Order Start Date",
            "end_date": "Order End Date",
            "item_type_field": "Item Type",
            "item_field": "Item",
            "cost_initial": "Initial Cost",
            "cost_week": "Cost Per Week"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.label_class = 'form-float-label'
        self.helper.layout = Layout(
            Fieldset(
                "Add a new order :",
                FloatingField('start_date',
                wrapper_class='col-md-3 mb-3 p-0'),
                FloatingField('end_date',
                wrapper_class='col-md-3 mb-3 p-0'),
                FloatingField('item_type_field',
                wrapper_class='col-md-5 mb-3 p-0'),
                FloatingField('item_field',
                wrapper_class='col-md-5 mb-3 p-0'),
                FloatingField('cost_initial',
                wrapper_class='col-md-5 mb-3 p-0'),
                FloatingField('cost_week',
                wrapper_class='col-md-5 mb-3 p-0')
            )
        )
                
