
from .models import Item, ItemType
from django import forms


class ItemForm(forms.ModelForm):
    """
    Defining the ItemForm, assigning correctly formatted
    labels to the fields and declaring the fields to display
    for creation.
    """
    class Meta:
        model = Item
        fields = ['item_type', 'item_serial']
        labels = {
            "item_type": "Type",
            "item_serial": "Serial No."
        }


class ItemTypeForm(forms.ModelForm):
    """
    Defining the ItemTypeForm, assigning correctly formatted
    labels to the fields and declaring the fields to display
    for creation.
    """
    class Meta:
        model = ItemType
        fields = ['name', 'category',
                  'cost_initial', 'cost_week', 'image']
        labels = {
            "name": "Type",
            "category": "Category",
            "cost_initial": "Initial (£)",
            "cost_week": "Weekly (£)",
            "image": "Image"
        }
