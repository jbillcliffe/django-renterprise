
from .models import Item, ItemType
from django import forms

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_type', 'item_serial']
        labels = {
            "item_type": "Type",
            "item_serial": "Serial No."
        }

class ItemTypeForm(forms.ModelForm):
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

