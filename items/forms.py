from .models import Item, ItemType
from django import forms

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('item_type', 'item_serial')