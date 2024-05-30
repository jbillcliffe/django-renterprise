
from .models import Item, ItemType
from django import forms

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_type', 'item_serial']
        labels = {
            "item_type": "Item Type",
            "item_serial": "Item Serial"
        }

class ItemTypeForm(forms.ModelForm):
    class Meta:
        model = ItemType
        fields = ['name', 'category',
            'cost_initial', 'cost_week', 'image']
        labels = {
            "name": "Item Type",
            "category": "Item Category",
            "cost_initial": "Initial Cost",
            "cost_week": "Cost Per Week",
            "image": "Item Image"
        }

