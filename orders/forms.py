from django import forms
from django.db.models import TextField
from django.db.models.functions import Cast
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import Order, OrderNote, Invoice
from items.models import Item, ItemType


# https://stackoverflow.com/questions/73789407/django-summernote-clean-got-an-unexpected-keyword-argument-styles-in-djangof
class OrderForm(forms.ModelForm):
    item_type_categories = ItemType.objects.values_list(
        "category",
        flat=True).order_by("category").distinct("category")

    item_type_names = ItemType.objects.values_list(
        "name",
        flat=True).order_by("name").distinct("name")

    item_type_names_hidden = ItemType.objects.values(
        "name", "category", "id",
        cost_initial_str=Cast('cost_initial', TextField()),
        cost_week_str=Cast('cost_week', TextField())).order_by(
            "name").distinct("name")

    orders_history = Order.objects.values(
        'item_id',
        start_date_str=Cast('start_date', TextField()),
        end_date_str=Cast('end_date', TextField()))

    # https://stackoverflow.com/questions/17085898/conversion-of-datetime-field-to-string-in-django-queryset-values-list
    # Casting the datetime.date fields to strings so they
    # can be parsed into JSON
    full_item_list = Item.objects.values(
        "id", "item_type", "item_serial", "status")
    item_type_field = forms.ModelChoiceField(
        item_type_categories, label="Category", required=False)
    # Set required to False on these fields. As display:none causes error
    # Validation occurs in JS.
    item_field = forms.ModelChoiceField(
        item_type_names, label="Item", required=False)
    item_field_hidden = forms.ModelChoiceField(
        item_type_names_hidden, required=False)
    full_item_hidden = forms.ModelChoiceField(
        full_item_list, required=False)
    orders_hidden = forms.ModelChoiceField(orders_history, required=False)

    class Meta:
        model = Order
        fields = [
            'item_type_field', 'item_field',
            'item_field_hidden', 'full_item_hidden',
            'orders_hidden', 'item', 'cost_initial',
            'cost_week', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.TextInput(attrs={'type': 'date'}),
            'end_date': forms.TextInput(attrs={'type': 'date'}),
        }
        labels = {
            "start_date": "Start Date",
            "end_date": "End Date",
            "item_type_field": "Item Type",
            "item_field": "Item",
            "cost_initial": "Initial (£)",
            "cost_week": "Weekly (£)"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs['autocomplete'] = 'off'
        self.helper.layout = Layout(
            Fieldset(
                "Add a new order",
                FloatingField(
                    'start_date',
                    wrapper_class='col-md-3 mb-3 p-0'),
                FloatingField(
                    'end_date',
                    wrapper_class='col-md-3 mb-3 p-0'),
                FloatingField(
                    'item_type_field',
                    wrapper_class='col-md-5 mb-3 p-0'),
                FloatingField(
                    'item_field',
                    wrapper_class='col-md-5 mb-3 p-0'),
                FloatingField(
                    'cost_initial',
                    wrapper_class='col-md-5 mb-3 p-0'),
                FloatingField(
                    'cost_week',
                    wrapper_class='col-md-5 mb-3 p-0')
            )
        )


class OrderNoteForm(forms.ModelForm):
    class Meta:
        model = OrderNote
        fields = ('note',)
        labels = {
            "note": "Note"
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        # order, created_on and status added in function not form
        model = Invoice
        fields = ('amount_paid', 'note',)
        labels = {
            "amount_paid": "Amount Paid",
            "note": "Note"
        }
