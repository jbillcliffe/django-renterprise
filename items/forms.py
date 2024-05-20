from .models import Item, ItemType
from django import forms

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('item_type', 'item_serial')

class ItemTypeForm(forms.ModelForm):
    class Meta:
        model = ItemType
        fields = ('name', 'category',
            'cost_initial', 'cost_week', 'image')